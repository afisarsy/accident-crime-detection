import os
import logging
import argparse
from datetime import datetime
from time import perf_counter
from typing import Callable

import numpy as np
import asyncio

from libs.nnmodule import NN
from libs.gpsmodule import GPS

logger = logging.getLogger(__name__)

#=================== Audio File Segmentation Task ===================
async def segmentaudio(options:argparse.Namespace, read_segment:Callable, status:Callable, model_config:dict):
    """
    Audio file segmentation task
    """
    
    while status():
        start_counter = perf_counter()
        logger.debug("Read segment from file")
        read_segment()
        await asyncio.sleep((model_config["segment duration"] * model_config["overlap ratio"] / 1000) - (perf_counter() - start_counter))

#===================== Feature Extraction Task ======================
async def featureextreaction(options:argparse.Namespace, get_segments:Callable, status:Callable, nn:NN, model_config:dict, path = ""):
    """
    Feature extraction task
    """
    #Load required Libraries
    from libs.audiomodule import Audio

    i = 0
    while status():
        start_counter = perf_counter()
        #Extract feature of available segments
        for segment in get_segments():
            #Apply bandpass filter
            logger.debug("Filtering segment")
            if options.log_process:
                time_start = datetime.now()
            filtered_segment = Audio.bandpassfilter(segment["segment"], model_config["sampling rate"], model_config["cutoff"], model_config["order"])

            #Calculate the mel spectrogram
            logger.debug("Calculating mel spectrogram")
            mel_spectrogram_db = Audio.getmelspectrogram(filtered_segment, model_config["sampling rate"], model_config["nfft"], model_config["hop length"], model_config["nmel"])

            #Normalization
            logger.debug("Data normalization")
            normalized_spectrogram_db = Audio.normalize(mel_spectrogram_db)

            if "rbir" in model_config and model_config["rbir"] is not None:
                feature = Audio.RbIR(normalized_spectrogram_db, model_config["rbir"])
            else:
                feature = normalized_spectrogram_db

            #Check input data
            logger.debug(feature)

            preprocessed_data = {
                "spectrogram" : feature,
                "time" : segment["time"]
            }
            if options.log_process:
                preprocessed_data["preprocessing start"] = time_start
                preprocessed_data["preprocessing finish"] = datetime.now()

            #Save spectrogram
            #For testing purpose
            #if path not None:
                #Audio.savemel(feature, path + "-" + str(i) + ".png")
                #logger.info("Spectrogram saved to %s", path + "-" + str(i) + ".png")

            #Add feature to buffer
            nn.add2buffer(preprocessed_data)

            i += 1

        await asyncio.sleep((model_config["segment duration"] * model_config["overlap ratio"] / 1000) - (perf_counter() - start_counter))


#========================== Detection Tasks =========================
async def detection(options:argparse.Namespace, status:Callable, nn:NN, th:float, model_config:dict, get_loc:Callable, mqtt_config:dict={}, mqtt_topic=""):
    """
    Classification and Thresholding task
    """
    #Initalize data handler
    from maindatahandler import DataHandler
    data_handler = DataHandler({
        "segment duration": model_config["segment duration"],
        "overlap ratio": model_config["overlap ratio"],
        "min alert duration": .1,          #in seconds,
        "min steady duration": 1,          #in seconds
        "gps tollerance": 10        #in meters
    })

    #Initialize MQTT if enabled
    if not options.no_mqtt:
        from libs.mqttmodule import MQTT
        mqtt_client = MQTT(conf=mqtt_config)

    #Initialize Logging to csv if enabled
    if options.log_process:
        import csv

        if not os.path.exists("Tests"):
            os.mkdir("Tests")
            
        process_log_path = "Tests/save_log_process"
        process_log_file = options.model[(options.model.rfind('/')+1):-3] + "_" + str(options.threshold) + "_" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".csv"
        log_process_file = open(process_log_path + "/" + process_log_file, 'w', newline='')

        #Write Header
        header = ["time", "preprocessing start", "preprocessing finish", "detection start", "detection finish", "prediction", "confidence", "conclusion"]
        csv_writer = csv.DictWriter(log_process_file, header)
        csv_writer.writeheader()

    while status():
        start_counter = perf_counter()
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

                #Get gps data if enabled
                gps_data = get_loc()

                #Data filtering
                data = {
                    "lat": gps_data["lat"],
                    "lng": gps_data["lng"],
                    "status": output,
                    "timestamp": buffer[i]["time"].strftime("%Y-%m-%d %H:%M:%S")
                }

                logger.info("Output : %s",output)
                if data_handler.submit(data):
                    logger.info("Result : %s", data)
                    if not options.no_mqtt:
                        mqtt_client.publishdata(mqtt_topic, data)

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
                    process_log["detection start"] = time_start
                    process_log["detection finish"] = time_finish
                    
                process_logs.append(process_log)
            
            if options.log_process:
                try:
                    csv_writer.writerows(process_logs)
                except AttributeError as e:
                    logger.error(e)

        await asyncio.sleep(0.01 - (perf_counter() - start_counter))

    #Disconnect MQTT
    if not options.no_mqtt:
        mqtt_client.stopmqtt()

    #Close csv file
    if options.log_process:
        log_process_file.close()


#============================= GPS Tasks ============================
async def gpsread(gps:GPS, status:Callable):
    """
    GPS reading task
    """
    #Initialize gps module
    while status():
        start_counter = perf_counter()
        gps.read_serial()

        #Update gps data every 5 seconds if gps is ready, 1 second if otherwise
        await asyncio.sleep((5 - (perf_counter() - start_counter)) if gps.ready else (1 - (perf_counter() - start_counter)))

    #Stop gps serial connection
    gps.stop()