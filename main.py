from pprint import pformat
import asyncio

from scipy.io.wavfile import write

from libs.configLoader import config
from libs.argParser import options
from libs.logger import getLogger
from libs.micHandler import Mic

logger = getLogger(__name__)
loop = asyncio.get_event_loop()

async def saveaudio(mic, sampling_rate, path):
    i = 0
    while True:
        for segment in mic.segments:
            logger.info("Saving audio data")
            write(path + "-" + str(i) + ".wav", sampling_rate, segment)
            logger.info("Data saved to %s", path + "-" + str(i) + ".wav")
            i += 1
        mic.segments = []
        await asyncio.sleep(0.5)

async def routines(mic):
    logger.info("Starting routines")
    #create audio stream task
    mic_stream_task = mic.startstream()
    audio_save_task = loop.create_task(saveaudio(mic, config["schemes"][options.scheme - 1]["sampling rate"], "Tests/save_audio/audio"))

    #wait all task excep routines
    await asyncio.gather(*asyncio.all_tasks() - {asyncio.current_task()})

def main():
    logger.info("Using scheme %i", options.scheme)
    logger.info("Scheme property : \n%s",pformat(config["schemes"][options.scheme - 1]))
    used_scheme = config["schemes"][options.scheme - 1]

    #mic initialization
    mic = Mic(used_scheme)
    mic.getdevices()
    mic.selectdevice(2)

    try:
        #start routines task
        loop.run_until_complete(routines(mic))
    finally:
        #close all task
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()

        #stop audio stream
        mic.stopstream()
        mic.destroy()

if __name__ == '__main__':
    main()