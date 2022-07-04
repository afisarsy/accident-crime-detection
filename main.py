import sys
from pprint import pformat
import asyncio

from libs.configloader import config
from libs.argparser import options
from libs.logger import getLogger
from libs.michandler import Mic
from libs.audiohandler import Audio

logger = getLogger(__name__)
loop = asyncio.get_event_loop()

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

            #Save spectrogram
            #For testing purpose
            Audio.savemel(normalized_spectrogram_db, path + "-" + str(i) + ".png")
            logger.info("Spectrogram saved to %s", path + "-" + str(i) + ".png")

            i += 1

        await asyncio.sleep(config["segment duration"] * config["overlap ratio"] / 1000)

def main():
    logger.info("Using scheme %i", options.scheme)
    logger.info("Scheme property : \n%s",pformat(config["schemes"][options.scheme - 1]))
    used_scheme = config["schemes"][options.scheme - 1]

    #mic initialization
    mic = Mic(used_scheme)
    mic.getdevices()
    mic.selectdevice(2)
    #start audio stream
    mic.startstream()

    #tasks declaration
    tasks = asyncio.gather(
        loop.create_task(featureextreaction(mic, used_scheme, "Tests/save_spectrogram/spectrogram"))
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