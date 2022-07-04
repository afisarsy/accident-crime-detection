import logging
from pprint import pformat
import asyncio

import numpy as np
import pyaudio

logger = logging.getLogger(__name__)

FORMAT=pyaudio.paFloat32
CHANNELS = 1

class Mic:
    """
    Microphone Object
    """
    
    #config
    config = {
        "arch": None,
        "sampling rate": 44100,
        "chunk duration": None,
        "overlap ratio": None,
        "cutoff": [],
        "order": None,
        "nfft": None,
        "hop length": None,
        "nmel": 128
    }

    #mic device params
    mic = None
    selected_device_index = 0
    info = None
    num_devices = 1
    available_devices = []

    #stream params
    stream = None
    chunks_per_segment = 20
    chunks = []
    streambits = None
    segments = []

    #async params
    loop = asyncio.get_event_loop()

    def __init__(self, conf):
        """
        Create Microphone Object
        """
        #Mic initialization
        self.mic = pyaudio.PyAudio()
        self.info = self.mic.get_host_api_info_by_index(0)
        self.num_devices = self.info.get('deviceCount')
        self.available_devices = [self.mic.get_device_info_by_host_api_device_index(0, i).get('name') for i in range(0, self.num_devices) if (self.mic.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 1]

        #Load scheme
        self.config["arch"] = conf["arch"]
        self.config["sampling rate"] = conf["sampling rate"]
        self.config["chunk duration"] = conf["chunk duration"]
        self.config["overlap ratio"] = conf["overlap ratio"]
        self.config["cutoff"] = conf["cutoff"]
        self.config["order"] = conf["order"]
        self.config["nfft"] = conf["nfft"]
        self.config["hop length"] = conf["hop length"]
        self.config["nmel"] = conf["nmel"]

        #Mic stream initialization
        self.streambits = int(self.config["sampling rate"] / self.chunks_per_segment)
        #Add silent segment
        silent_chunk = (np.zeros(self.streambits)).astype(np.float32)
        for i in range(0, self.chunks_per_segment):
            self.chunks.append(silent_chunk)


    def getdevices(self):
        """
        List available audio input devices
        """
        for i in range(0, len(self.available_devices)):
            logger.debug("Input Device id %i - %s", i, self.available_devices[i])
    
    def selectdevice(self, id):
        """
        Select audio input device to be used
        """
        if id >= len(self.available_devices) or id < 0:
            devices = {i: self.available_devices[i] for i in range(0, len(self.available_devices))}
            logger.warning(
                "Device with id %i not available, available devices:\n %s", id, pformat(devices)
            )
            return 0
        self.selected_device_index = id
        self.getselecteddevice()
    
    def getselecteddevice(self):
        """
        Return selected audio input device info
        """
        logger.info(
            "Selected device %i - %s", self.selected_device_index, self.available_devices[self.selected_device_index]
        )
        return {self.selected_device_index: self.available_devices[self.selected_device_index]}
    
    def startstream(self):
        """
        Start streaming selected audio input
        """
        logger.info("Initializing streamer")
        self.stream = self.mic.open(format = FORMAT,
            channels = CHANNELS,
            rate = self.config["sampling rate"],
            frames_per_buffer = self.config["chunk duration"],
            output = False,
            input = True,
            input_device_index = self.selected_device_index
        )
        logger.info("Starting audio stream")
        self.stream.start_stream()
        logger.info("Stream started using device %i - %s", self.selected_device_index, self.available_devices[self.selected_device_index])
        mic_stream_task = self.loop.create_task(self.getstreamdata())
        return mic_stream_task
    
    def stopstream(self):
        """
        Stop audio input stream
        """
        logger.info("Stopping stream")
        #self.loop.get_task_factory

        #stop audio input stream
        self.stream.stopstream()
        self.stream.close()
        logger.info("Stream stopped")

    async def getstreamdata(self):
        i = 0
        while True:
            data = self.stream.read(self.streambits)
            self.chunks.append(data)
            self.chunks.pop(0)
            i += 1
            if i >= int(self.chunks_per_segment * self.config["overlap ratio"]):
                i = 0
                self.createsegment()
                logger.info("Audio segment created")
    
    def createsegment(self):
        self.segments.append(np.frombuffer(b''.join(self.chunks), np.float32))

    def destroy(self):
        self.mic.terminate()