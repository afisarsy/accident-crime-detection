import logging
from pprint import pformat

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
        "segment duration": None,
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
    num_devices = 0
    available_devices = []

    #stream params
    stream = None
    CHUNKS_PER_SEGMENT = 20
    chunks = []
    CHUNK_COUNTER = 0
    streambits = None
    segments = []

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
        self.config["segment duration"] = conf["segment duration"]
        self.config["overlap ratio"] = conf["overlap ratio"]
        self.config["cutoff"] = conf["cutoff"]
        self.config["order"] = conf["order"]
        self.config["nfft"] = conf["nfft"]
        self.config["hop length"] = conf["hop length"]
        self.config["nmel"] = conf["nmel"]

        #Mic stream initialization
        self.streambits = int(self.config["sampling rate"] / self.CHUNKS_PER_SEGMENT)
        #Add silent segment
        silent_chunk = (np.zeros(self.streambits)).astype(np.float32)
        for i in range(0, int(self.CHUNKS_PER_SEGMENT * (self.config["segment duration"] / 1000))):
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
    
    def streamdatacallback(self, data, frame_count, time_info, status):
        self.chunks.append(data)
        self.chunks.pop(0)
        self.CHUNK_COUNTER += 1
        if self.CHUNK_COUNTER >= int(self.CHUNKS_PER_SEGMENT * self.config["overlap ratio"] * (self.config["segment duration"] / 1000)):
            #Save collected chunks with total duration = config["segment duration"]
            self.segments.append(np.frombuffer(b''.join(self.chunks), np.float32))
            logger.info("Audio segment created")

            self.CHUNK_COUNTER = 0
        return data, pyaudio.paContinue

    def startstream(self):
        """
        Start streaming selected audio input
        """
        logger.info("Initializing streamer")
        self.stream = self.mic.open(format = FORMAT,
            channels = CHANNELS,
            rate = self.config["sampling rate"],
            frames_per_buffer = self.streambits,
            output = False,
            input = True,
            input_device_index = self.selected_device_index,
            stream_callback = self.streamdatacallback
        )
        logger.info("Starting audio stream")
        self.stream.start_stream()
        logger.info("Stream started using device %i - %s", self.selected_device_index, self.available_devices[self.selected_device_index])

    def stopstream(self):
        """
        Stop audio input stream
        """
        #stop audio input stream
        logger.info("Stopping stream")
        self.stream.stop_stream()
        self.stream.close()
        logger.info("Stream stopped")
    
    def popallsegments(self):
        """
        Pop all available segments
        """
        popped_segments, self.segments = self.segments, []
        return popped_segments

    def destroy(self):
        self.mic.terminate()