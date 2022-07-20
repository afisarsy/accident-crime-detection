import argparse
from asyncore import write
import logging
from pprint import pformat
from datetime import datetime
import asyncio
import csv

from libs.argparser import parser, checkthreshold
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
    options = initargparser()
    initlogger(options.log)
    config = loadconfig(options.model)
    custom_objects = {"Rot90" : Rot90}
    process_log_path = "Tests/save_log_process"
    process_log_file = options.model[(options.model.rfind('/')+1):-3] + "_" + str(options.threshold) + "_" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".csv"

    logger.info("Using model %s", options.model)
    logger.info("Config : \n%s",pformat(config))

    #Log process initialization
    csv_writer = None
    if options.log_process:
        log_process_file = open(process_log_path + "/" + process_log_file, 'w', newline='')
        #Write Header
        header = ["time", "preprocessing start", "preprocessing finish", "detection start", "detection finish", "conclusion"]
        csv_writer = csv.DictWriter(log_process_file, header)
        csv_writer.writeheader()

    #mic initialization
    mic = Mic(config)
    mic.getdevices()
    mic.selectdevice(2)
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
        loop.create_task(detection(mic, nn, options.threshold, csv_writer=csv_writer, log_process=options.log_process))
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

            #Check input data
            logger.debug(normalized_spectrogram_db)

            preprocessed_data = {
                "spectrogram" : normalized_spectrogram_db,
                "time" : segment["time"]
            }
            if log_process:
                preprocessed_data["preprocessing start"] = time_start
                preprocessed_data["preprocessing finish"] = datetime.now()

            #Save spectrogram
            #For testing purpose
            #if path not None:
                #Audio.savemel(normalized_spectrogram_db, path + "-" + str(i) + ".png")
                #logger.info("Spectrogram saved to %s", path + "-" + str(i) + ".png")

            #Add feature to buffer
            nn.add2buffer(preprocessed_data)

            i += 1

        await asyncio.sleep(config["segment duration"] * config["overlap ratio"] / 1000)

async def detection(mic, nn, th, csv_writer = None, log_process = False):
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
                    "conclusion" : result,
                    "time" : buffer[i]["time"],
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

def initargparser():
    parser.add_argument(
        "model",
        metavar="MODEL_PATH",
        help=(
            "Provide model path. "
            "MODEL_PATH must contain config.file. "
        ),
    )
    parser.add_argument(
        "threshold",
        metavar="TH",
        type=checkthreshold,
        help=(
            "Provide threhold value. "
            "TH must be a float between (0.0-1.0). "
        ),
    )
    parser.add_argument(
        "--log-process",
        action="store_true",
        help=(
            "Log processing time into xml file."
        )
    )
    options = parser.parse_args()
    options.model = options.model.replace("\\","/")

    return options

if __name__ == '__main__':
    main()