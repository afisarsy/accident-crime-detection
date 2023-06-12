import logging
import argparse

logger = logging.getLogger(__name__)

def testmqtt(options:argparse.Namespace):
    """
    MQTT test
    """
    logger.info("MQTT test")
    #Load required Libraries
    from libs.mqttmodule import MQTT
    from datetime import datetime
    from libs.deviceinfo import device
    config = {
        "host": options.host,
        "port": options.port
    }
    mqtt_client = MQTT(conf=config)
    data = {
        "lat": 1.32131331,
        "lng": 0.42131312,
        "status": "normal",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    try:
        while(not mqtt_client.connected):
            pass
        logger.info("Sendind data with topic {}\n\t\t\t\t\t\t\t  - Data: {}".format(options.topic + device.getid(), data))
        mqtt_client.publishdata(options.topic, data)
        logger.info("Data Sent")
        logger.info("Press Ctrl+C to exit")
        while(mqtt_client.connected):
            pass
    except KeyboardInterrupt as e:
        pass
    finally:
        mqtt_client.stopmqtt()

def testgps(options:argparse.Namespace):
    """
    GPS test
    """
    logger.info("GPS test")
    #Load required Libraries
    from libs.gpsmodule import GPS
    from time import sleep
    
    gps_config = {
        "port": options.port,
        "baudrate": options.baudrate
    }
    logger.info(gps_config)
    gps = GPS(gps_config)
    sleep(1)
    gps.read_serial()
    logger.info(gps.get_lat_lng())
    gps.stop()

def testinferreal(options:argparse.Namespace):
    """
    Real-time like inference test
    """
    logger.info("Real-time like inference test")
    #Load required Libraries
    import asyncio
    from libs.audiohandler import AudioHandler
    from libs.configmodule import loadconfig
    from libs.nnmodule import NN, Rot90
    from libs.gpsmodule import GPS

    options.log_process = True
    options.no_mqtt = False

    loop = asyncio.get_event_loop()

    device_id = '100000006a71f8bb'

    #MQTT config
    mqtt_config = {
        "host": "103.106.72.182",
        "port": 1887,
        "device_id": device_id
    }
    mqtt_topics = {
        "data": "acd/node/",
        "test": "acd/test/"
    }

    #Model Initialization
    options.model = options.model.replace("\\","/")
    model_config = loadconfig(options.model)
    custom_objects = {"Rot90" : Rot90}

    #Output mapper
    output_map = {
        "conversation" : "normal",
        "engine_idling" : "normal",
        "rain" : "normal",
        "road_traffic" : "normal",
        "thunderstorm" : "normal",
        "wind" : "normal",
        "car_crash" : "accident",
        "gun_shot" : "crime",
        "jambret" : "crime",
        "maling" : "crime",
        "rampok" : "crime",
        "scream" : "crime",
        "tolong" : "crime"
    }

    #NN initialization
    nn = NN(options.model, custom_objects, output_map, model_config)

    #Audio initialization
    audio = AudioHandler(model_config)
    audio.loadwav(options.filename)

    #tasks declaration
    from maintasks import segmentaudio, featureextreaction, detection
    tasks = asyncio.gather(
        loop.create_task(segmentaudio(options, audio.readsegment, audio.isactive, model_config)),
        loop.create_task(featureextreaction(options, audio.popallsegments, audio.isactive, nn, model_config, "Tests/save_spectrogram/spectrogram")),
        loop.create_task(detection(options, audio.isactive, nn, options.threshold, model_config, GPS.get_dumped_gps_data, mqtt_config, mqtt_topic=mqtt_topics["test"]))
    )

    try:
        #start routines task
        loop.run_until_complete(tasks)

    except KeyboardInterrupt as e:
        #stop audio stream
        audio.stop()

    finally:
        #close all task
        loop.run_until_complete(loop.shutdown_asyncgens())

def testinfer(options:argparse.Namespace):
    """
    Inference test
    """
    logger.info("Inference test")
    #Load required Libraries
    import os
    import glob
    import csv
    from datetime import datetime
    from libs.audiohandler import AudioHandler
    from libs.audiomodule import Audio
    from libs.configmodule import loadconfig
    from libs.nnmodule import NN, Rot90
    from maindatahandler import DataHandler
    import numpy as np

    #Tested files path
    files = [
        "Tests/8 real_data_test/1.0m_1m.wav",
        "Tests/8 real_data_test/1.0m_3m.wav",
        "Tests/8 real_data_test/1.0m_5m.wav",
        "Tests/8 real_data_test/1.5m_1m.wav",
        "Tests/8 real_data_test/1.5m_3m.wav",
        "Tests/8 real_data_test/1.5m_5m.wav"
    ]

    #Threshold values
    ths = [.4, .5, .6, .7, .75, .8, .85, .9]
    #Output mapper
    output_map = {
        "conversation" : "normal",
        "engine_idling" : "normal",
        "rain" : "normal",
        "road_traffic" : "normal",
        "thunderstorm" : "normal",
        "wind" : "normal",
        "car_crash" : "accident",
        "gun_shot" : "crime",
        "jambret" : "crime",
        "maling" : "crime",
        "rampok" : "crime",
        "scream" : "crime",
        "tolong" : "crime"
    }

    #Model Initialization
    custom_objects = {"Rot90" : Rot90}
    options.models_dir = options.models_dir.replace("\\","/")
    process_log_path = "Tests/9 infer_test/{models_dir}".format(models_dir = options.models_dir[options.models_dir.rfind('/')+1:])
    #Check path
    if not os.path.exists(process_log_path):
        os.makedirs(process_log_path)

    glob_path = "{path}/*.h5".format(path = options.models_dir.replace("[","~").replace("]",":").replace("~","[[]").replace(":","[]]"))
    models = glob.glob(glob_path)

    errors = []
    try:
        for model in models:
            #NN initialization
            model = model.replace("\\","/")
            model_config = loadconfig(model)
            nn = NN(model, custom_objects, output_map, model_config)
            logger.info("Model: {}".format(model))

            #loop each files
            for filename in files:
                #Audio initialization
                logger.info("\tTest file: {}".format(filename))
                audio = AudioHandler(model_config)
                audio.loadwav(filename)
                audio.readallsegments()

                #Data handler initialization
                data_handlers = []
                data_handlers_results = []
                for th in ths:
                    data_handler = DataHandler({
                        "segment duration": model_config["segment duration"],
                        "overlap ratio": model_config["overlap ratio"],
                        "min duration": .5,          #in seconds
                    })
                    data_handlers.append(data_handler)
                    
                    data_handlers_results.append([])

                #Feature extraction
                logger.info("\t\tExtracting features")
                for segment in audio.popallsegments():
                    filtered_segment = Audio.bandpassfilter(segment["segment"], model_config["sampling rate"], model_config["cutoff"], model_config["order"])
                    mel_spectrogram_db = Audio.getmelspectrogram(filtered_segment, model_config["sampling rate"], model_config["nfft"], model_config["hop length"], model_config["nmel"])
                    normalized_spectrogram_db = Audio.normalize(mel_spectrogram_db)

                    if "rbir" in model_config and model_config["rbir"] is not None:
                        feature = Audio.RbIR(normalized_spectrogram_db, model_config["rbir"])
                    else:
                        feature = normalized_spectrogram_db
                    nn.add2buffer(feature)
                
                #Inference
                logger.info("\t\tInference")
                nn_predictions = nn.predict(nn.popallbuffer())

                outputs = []
                for i, nn_prediction in enumerate(nn_predictions):
                    conclusions = {}
                    for j, th in enumerate(ths):
                        #Thresholding
                        result = nn.thresholding(nn_prediction, th)

                        #Map result using output map
                        conclusion = nn.mapresult(result)
                        conclusions.update({"th {}".format(th) : conclusion})

                        #Data handler
                        if data_handlers[j].submit({"status": conclusion}):
                            data_handlers_results[j].append({
                                "th {} index".format(th) : i,
                                "th {} status".format(th) : conclusion
                            })

                    #Comprehend data
                    outputs.append(conclusions)
                
                #Process logging
                process_logs = []
                for i, output in enumerate(outputs):
                    process_log = {
                        "prediction" : nn.getclass(nn_predictions[i]),
                        "confidence" : np.max(nn_predictions[i])
                    }
                    process_log.update(output)                    
                    process_logs.append(process_log)
                            
                process_log_file = "{model}_[{filename}]_{date}.csv".format(model = model[(model.rfind('/')+1):-3], filename = filename[filename.rfind('/')+1:-4], date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))

                with open(process_log_path + "/" + process_log_file, 'w', newline='') as log_process_file:
                    #Write Header
                    header = ["prediction", "confidence"] + ["th {}".format(th) for th in ths]
                    csv_writer = csv.DictWriter(log_process_file, header)
                    csv_writer.writeheader()
                    try:
                        csv_writer.writerows(process_logs)
                        logger.info("\t\tSaved to: {}".format(process_log_file))
                    except AttributeError as e:
                        logger.error(e)
                
                #Status logging
                data_handler_log = []
                for i in range(len(max(data_handlers_results, key=len))):
                    row = {}
                    for j, data_handler_result in enumerate(data_handlers_results):
                        default = {
                            "th {} index".format(ths[j]) : "",
                            "th {} status".format(ths[j]): "",
                        }
                        data_handler_result_data = data_handler_result[i] if i < len(data_handler_result) else default
                        row.update(data_handler_result_data)
                    data_handler_log.append(row)
                data_handler_log_file = process_log_file[:process_log_file.rfind('.csv')] + "_datahandler.csv"

                with open(process_log_path + "/" + data_handler_log_file, 'w', newline='') as log_data_handler_file:
                    #Write Header
                    header = [head for th in ths for head in ["th {} index".format(th)] + ["th {} status".format(th)]]
                    csv_writer = csv.DictWriter(log_data_handler_file, header)
                    csv_writer.writeheader()
                    try:
                        csv_writer.writerows(data_handler_log)
                        logger.info("\t\tSaved to: {}".format(data_handler_log_file))
                    except AttributeError as e:
                        logger.error(e)
    except Exception as e:
        errors.append(e)
    
    for i in errors:
        logger.error(i)