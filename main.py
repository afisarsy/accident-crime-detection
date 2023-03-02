import json
import logging
from pprint import pformat
from datetime import datetime
import asyncio

import numpy as np

from mainparser import parser
from libs.logger import initlogger
from libs.deviceinfo import device

logger = logging.getLogger(__name__)
loop = asyncio.get_event_loop()

def main():
    """
    Audio-based detection and crime detection system
    Realtime runtime system
    """

    options = parser.parse_known_args()[0]
    initlogger(options.log)

    if str.lower(options.mode) == "run":
        running()
    elif str.lower(options.mode) == "get":
        getparam()

def running():
    #Load required Libraries
    from libs.configmodule import loadconfig
    from libs.michandler import Mic
    from libs.nnmodule import NN, Rot90

    options = parser.parse_args()

    #Model Initialization
    options.model = options.model.replace("\\","/")
    config = loadconfig(options.model)
    custom_objects = {"Rot90" : Rot90}

    logger.info("Using model %s", options.model)
    logger.info("Loading Config File\nConfig : \n%s",pformat(config))

    #MQTT initialization
    mqtt_config = {
        "host": "103.106.72.182",
        "port": 1887
    }
    mqtt_topics = {
        "data": "acd/node/",
        "test": "acd/test/"
    }

    #mic initialization
    mic = Mic(config)
    mic.selectdevice(options.mic)
    mic.getselecteddevice()
    #start audio stream
    mic.startstream()

    #Output mapper
    output_map = {
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
    nn = NN(options.model, custom_objects, output_map, config)

    #tasks declaration
    tasks = asyncio.gather(
        loop.create_task(featureextreaction(mic, nn, config, options, "Tests/save_spectrogram/spectrogram")),
        loop.create_task(detection(mic, nn, options.threshold, config, options, mqtt_config=mqtt_config, mqtt_topic=mqtt_topics["test"]))
    )

    try:
        #start routines task
        loop.run_until_complete(tasks)

    except KeyboardInterrupt as e:
        #stop audio stream
        mic.stopstream()
        mic.destroy()

    finally:
        #close all task
        loop.run_until_complete(loop.shutdown_asyncgens())
        #loop.close()

async def featureextreaction(mic, nn, config, options, path = None):
    """
    Feature extraction task
    """
    #Load required Libraries
    if 'Audio' not in dir():
        from libs.audiomodule import Audio

    i = 0
    while mic.stream.is_active():
        #Extract feature of available segments
        for segment in mic.popallsegments():
            #Apply bandpass filter
            logger.debug("Filtering segment")
            if options.log_process:
                time_start = datetime.now()
            filtered_segment = Audio.bandpassfilter(segment["segment"], config["sampling rate"], config["cutoff"], config["order"]) # type: ignore

            #Calculate the mel spectrogram
            logger.debug("Calculating mel spectrogram")
            mel_spectrogram_db = Audio.getmelspectrogram(filtered_segment, config["sampling rate"], config["nfft"], config["hop length"], config["nmel"]) # type: ignore

            #Normalization
            logger.debug("Data normalization")
            normalized_spectrogram_db = Audio.normalize(mel_spectrogram_db) # type: ignore

            if config["rbir"] is not None:
                feature = Audio.RbIR(normalized_spectrogram_db, config["rbir"]) # type: ignore
            else:
                feature = normalized_spectrogram_db

            #Check input data
            logger.debug(feature)

            preprocessed_data = {
                "spectrogram" : feature,
                "time" : segment["time"]
            }
            if options.log_process:
                preprocessed_data["preprocessing start"] = time_start # type: ignore
                preprocessed_data["preprocessing finish"] = datetime.now()

            #Save spectrogram
            #For testing purpose
            #if path not None:
                #Audio.savemel(feature, path + "-" + str(i) + ".png")
                #logger.info("Spectrogram saved to %s", path + "-" + str(i) + ".png")

            #Add feature to buffer
            nn.add2buffer(preprocessed_data)

            i += 1

        await asyncio.sleep(config["segment duration"] * config["overlap ratio"] / 1000)

async def detection(mic, nn, th, config, options, mqtt_config={}, mqtt_topic=""):
    """
    Classification and Thresholding task
    """
    #Initalize data handler
    from maindatahandler import DataHandler
    data_handler = DataHandler({
        "segment duration": config["segment duration"],
        "overlap ratio": config["overlap ratio"],
        "min duration": 1,          #in seconds
        "gps tollerance": 10        #in meters
    })

    #Initialize MQTT if enabled
    if not options.no_mqtt:
        from libs.mqttmodule import MQTT
        mqtt_client = MQTT(conf=mqtt_config)

    #Initialize Logging to csv if enabled
    if options.log_process:
        import csv

        process_log_path = "Tests/save_log_process"
        process_log_file = options.model[(options.model.rfind('/')+1):-3] + "_" + str(options.threshold) + "_" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".csv"
        log_process_file = open(process_log_path + "/" + process_log_file, 'w', newline='')

        #Write Header
        header = ["time", "preprocessing start", "preprocessing finish", "detection start", "detection finish", "prediction", "confidence", "conclusion"]
        csv_writer = csv.DictWriter(log_process_file, header)
        csv_writer.writeheader()

    while mic.stream.is_active():
        #Classification
        buffer = nn.popallbuffer()
        if len(buffer) > 0:
            logger.info("Predicting %i batch of data", len(buffer))
            if options.log_process:
                time_start = datetime.now()
            nn_predictions = nn.predict([data["spectrogram"] for data in buffer])
            #logger.debug("Prediction %s", nn_predictions)

            outputs = []
            for i, nn_prediction in enumerate(nn_predictions):
                #Thresholding
                result = nn.thresholding(nn_prediction, th)

                #Map result using output map
                output = nn.mapresult(result)

                #Data filtering
                data = {
                    "lat": 1.32131331,
                    "lng": 0.42131312,
                    "status": output,
                    "timestamp": buffer[i]["time"].strftime("%Y-%m-%d %H:%M:%S")
                }

                if data_handler.submit(data):
                    logger.info("Result : %s", data)
                    if not options.no_mqtt:
                        mqtt_client.publishdata(mqtt_topic, data) # type: ignore

                #Comprehend data
                outputs.append(output)

            #Logging
            if options.log_process:
                time_finish = datetime.now()
            process_logs = []
            for i, output in enumerate(outputs):
                process_log = {
                    "time" : buffer[i]["time"],
                    "prediction" : nn.getclass(nn_predictions[i]),
                    "confidence" : np.max(nn_predictions[i]),
                    "conclusion" : output
                }
                if options.log_process:
                    process_log["preprocessing start"] = buffer[i]["preprocessing start"]
                    process_log["preprocessing finish"] = buffer[i]["preprocessing finish"]
                    process_log["detection start"] = time_start # type: ignore
                    process_log["detection finish"] = time_finish # type: ignore
                    
                process_logs.append(process_log)
            
            if options.log_process:
                try:
                    csv_writer.writerows(process_logs) # type: ignore
                except AttributeError as e:
                    logger.error(e)

        await asyncio.sleep(0.01)

    #Disconnect MQTT
    if not options.no_mqtt:
        mqtt_client.stopmqtt() # type: ignore

    #Close csv file
    if options.log_process:
        log_process_file.close() # type: ignore

def getparam():
    #Load required Libraries
    from libs.michandler import Mic

    options = parser.parse_args()

    if options.param == "mic":
        available_devices = Mic.getdevices()
        logger.info("Get I/O Devices\nAvailable audio input : \n%s", pformat(available_devices))
    elif options.param == "id":
        logger.info("Get Device ID\nDevice ID : %s", device.getid())

if __name__ == '__main__':
    main()