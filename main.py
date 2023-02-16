import logging
from pprint import pformat
from datetime import datetime
import asyncio
import csv
import sys

import numpy as np

from libs.argparser import parser, Range
from libs.logger import initlogger
from libs.configmodule import loadconfig
from libs.michandler import Mic
from libs.audiomodule import Audio
from libs.nnmodule import NN, Rot90

logger = logging.getLogger(__name__)
loop = asyncio.get_event_loop()

def main():
    """
    Audio-based detection and crime detection system
    Realtime runtime system
    """
    initargs()    
    options = parser.parse_known_args()[0]
    initlogger(options.log)

    if str.lower(options.mode) == "run":
        running()
    elif str.lower(options.mode) == "get":
        get()

def running():
    options = parser.parse_args()

    options.model = options.model.replace("\\","/")
    config = loadconfig(options.model)
    custom_objects = {"Rot90" : Rot90}
    process_log_path = "Tests/save_log_process"
    process_log_file = options.model[(options.model.rfind('/')+1):-3] + "_" + str(options.threshold) + "_" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".csv"

    logger.info("Using model %s", options.model)
    logger.info("Loading Config File\nConfig : \n%s",pformat(config))

    #Log process initialization
    csv_writer = None
    if options.log_process:
        log_process_file = open(process_log_path + "/" + process_log_file, 'w', newline='')
        #Write Header
        header = ["time", "preprocessing start", "preprocessing finish", "detection start", "detection finish", "prediction", "confidence", "conclusion"]
        csv_writer = csv.DictWriter(log_process_file, header)
        csv_writer.writeheader()

    #mic initialization
    mic = Mic(config)
    mic.selectdevice(options.mic_index)
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
        loop.create_task(featureextreaction(mic, nn, config, "Tests/save_spectrogram/spectrogram", log_process=options.log_process)),
        loop.create_task(detection(mic, nn, options.threshold, config, csv_writer=csv_writer, log_process=options.log_process))
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
        loop.close()

        #Close csv file
        log_process_file.close()

async def featureextreaction(mic, nn, config, path = None, log_process = False):
    """
    Feature extraction task
    """
    i = 0
    while mic.stream.is_active():
        #Extract feature of available segments
        for segment in mic.popallsegments():
            #Apply bandpass filter
            logger.debug("Filtering segment")
            if log_process:
                time_start = datetime.now()
            filtered_segment = Audio.bandpassfilter(segment["segment"], config["sampling rate"], config["cutoff"], config["order"])

            #Calculate the mel spectrogram
            logger.debug("Calculating mel spectrogram")
            mel_spectrogram_db = Audio.getmelspectrogram(filtered_segment, config["sampling rate"], config["nfft"], config["hop length"], config["nmel"])

            #Normalization
            logger.debug("Data normalization")
            normalized_spectrogram_db = Audio.normalize(mel_spectrogram_db)

            if config["rbir"] is not None:
                feature = Audio.RbIR(normalized_spectrogram_db, config["rbir"])
            else:
                feature = normalized_spectrogram_db

            #Check input data
            logger.debug(feature)

            preprocessed_data = {
                "spectrogram" : feature,
                "time" : segment["time"]
            }
            if log_process:
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

        await asyncio.sleep(config["segment duration"] * config["overlap ratio"] / 1000)

async def detection(mic, nn, th, config, csv_writer = None, log_process = False):
    """
    Classification and Thresholding task
    """
    while mic.stream.is_active():
        #Classification
        buffer = nn.popallbuffer()
        if len(buffer) > 0:
            logger.info("Predicting %i batch of data", len(buffer))
            if log_process:
                time_start = datetime.now()
            y = nn.predict([data["spectrogram"] for data in buffer])
            #logger.debug("Prediction %s", y)

            #Thresholding
            results = nn.thresholding(y, th)
            if log_process:
                time_finish = datetime.now()
            outputs = []
            for i, result in enumerate(results):
                output = {
                    "time" : buffer[i]["time"],
                    "prediction" : config["classes"][np.argmax(y[i])],
                    "confidence" : np.max(y[i]),
                    "conclusion" : result
                }
                if log_process:
                    output["preprocessing start"] = buffer[i]["preprocessing start"]
                    output["preprocessing finish"] = buffer[i]["preprocessing finish"]
                    output["detection start"] = time_start
                    output["detection finish"] = time_finish
                    
                outputs.append(output)
            
            if log_process:
                try:
                    csv_writer.writerows(outputs)
                except AttributeError as e:
                    logger.error(e)

            logger.info("Result : %s", outputs)

        await asyncio.sleep(0.01)

def get():
    options = parser.parse_args()

    if options.param == "mic":
        available_devices = Mic.getdevices()
        logger.info("Get I/O Devices\nAvailable audio input : \n%s", pformat(available_devices))

def initargs():
    #Subparsers
    subparsers = parser.add_subparsers(
        title="Program MODE",
        dest="mode",
        metavar="MODE",
        required=True,
        description="Select Program Mode",
        help=(
            "Available MODE [run, get]."
        )
    )

    #Running arguments
    parser_run = subparsers.add_parser("run", aliases=["RUN"])
    parser_run.add_argument(
        "model",
        metavar="MODEL_PATH",
        help=(
            "Provide model path. "
            "MODEL_PATH must contain config.file. "
        ),
    )
    parser_run.add_argument(
        "threshold",
        metavar="TH",
        type=float,
        choices=[Range(0.0, 1.0)],
        help=(
            "Provide threhold value. "
            "TH must be a float between (0.0-1.0). "
        ),
    )
    parser_run.add_argument(
        "-mic",
        "--mic-index",
        metavar="MIC_INDEX",
        type=int,
        default=0,
        help=(
            "Select used microphone index from available microphone devices. "
            "Use  main.py GET MIC  to get available microphone devices"
        ),
    )
    parser_run.add_argument(
        "--log-process",
        action="store_true",
        help=(
            "Log processing time into xml file."
        )
    )

    #Get arguments
    parser_get = subparsers.add_parser('get', aliases=["GET"])
    getparams = ["mic"]
    parser_get.add_argument(
        "param",
        metavar="PARAM",
        type=str.lower,
        choices=getparams,
        help=(
            "Provide parameter you want to get. "
            "Available PARAM %s" % {' , '.join(getparams)}
        ),
    )

if __name__ == '__main__':
    main()