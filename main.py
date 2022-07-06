import argparse
import logging
from pprint import pformat
import asyncio

from libs.argparser import checkthreshold, checkloglevel
from libs.logger import initlogger
from libs.configloader import loadconfig
from libs.michandler import Mic
from libs.audiomodule import Audio

def initargparser():
    parser = argparse.ArgumentParser()
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
        "-get",
        default=None,
        help=(
            "Provide required data. "
            "Available options [schemes]. "
        )
    )
    parser.add_argument(
        "-log",
        "--log",
        type=checkloglevel,
        default="info",
        help=(
            "Provide logging level. "
            "Example --log debug, default='warning'"
        )
    )
    options = parser.parse_args()
    options.model = options.model.replace("\\","/")

    return options

async def featureextreaction(mic, config, path):
    """
    Feature extraction task
    """
    i = 0
    while mic.stream.is_active():
        #Extract feature of available segments
        for segment in mic.popallsegments():
            #Apply bandpass filter
            logger.info("Filtering segment")
            filtered_segment = Audio.bandpassfilter(segment, config["sampling rate"], config["cutoff"], config["order"])

            #Calculate the mel spectrogram
            logger.info("Calculating mel spectrogram")
            mel_spectrogram_db = Audio.getmelspectrogram(filtered_segment, config["sampling rate"], config["nfft"], config["hop length"], config["nmel"])

            #Normalization
            logger.info("Data normalization")
            normalized_spectrogram_db = Audio.normalize(mel_spectrogram_db)

            #Check input data
            logger.debug(normalized_spectrogram_db)

            #Save spectrogram
            #For testing purpose
            Audio.savemel(normalized_spectrogram_db, path + "-" + str(i) + ".png")
            logger.info("Spectrogram saved to %s", path + "-" + str(i) + ".png")

            i += 1

        await asyncio.sleep(config["segment duration"] * config["overlap ratio"] / 1000)

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

    logger.info("Using model %s", options.model)
    logger.info("Config : \n%s",pformat(config))

    #mic initialization
    mic = Mic(config)
    mic.getdevices()
    mic.selectdevice(2)
    #start audio stream
    mic.startstream()

    #tasks declaration
    tasks = asyncio.gather(
        loop.create_task(featureextreaction(mic, config, "Tests/save_spectrogram/spectrogram"))
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

if __name__ == '__main__':
    main()