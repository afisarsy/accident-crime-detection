from pprint import pformat
import asyncio

from scipy.io.wavfile import write

from libs.configloader import config
from libs.argparser import options
from libs.logger import getLogger
from libs.michandler import Mic

logger = getLogger(__name__)
loop = asyncio.get_event_loop()

async def saveaudio(mic, sampling_rate, path):
    i = 0
    while mic.stream.is_active():
        for segment in mic.popallsegments():
            logger.info("Saving audio data")
            write(path + "-" + str(i) + ".wav", sampling_rate, segment)
            logger.info("Data saved tas %s", path + "-" + str(i) + ".wav")
            i += 1
        await asyncio.sleep(mic.config["segment duration"] * mic.config["overlap ratio"] / 1000)

async def featureextreaction(mic):
    while mic.stream.is_active():
        for segment in mic.popallsegments():
            pass
        await asyncio.sleep(mic.config["segment duration"] * mic.config["overlap ratio"] / 1000)

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
        loop.create_task(saveaudio(mic, config["schemes"][options.scheme - 1]["sampling rate"], "Tests/save_audio/audio"))
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