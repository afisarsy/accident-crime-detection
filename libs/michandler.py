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
    __config = {
        "sampling rate": 44100,
        "segment duration": None,
        "overlap ratio": None
    }

    #mic device params
    __mic = None
    __selected_device_index = 0
    __info = None
    __num_devices = 0
    __available_devices = []

    #stream params
    stream = None
    __CHUNKS_PER_SEGMENT = 20
    __chunks = []
    __CHUNK_COUNTER = 0
    __streambits = None
    __segment = []

    def __init__(self, conf):
        """
        Create Microphone Object
        """
        #Mic initialization
        self.__mic = pyaudio.PyAudio()
        self.__info = self.__mic.get_host_api_info_by_index(0)
        self.__num_devices = self.__info.get('deviceCount')
        self.__available_devices = [self.__mic.get_device_info_by_host_api_device_index(0, i).get('name') for i in range(0, self.__num_devices) if (self.__mic.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 1]

        #Load scheme
        self.__config["sampling rate"] = conf["sampling rate"]
        self.__config["segment duration"] = conf["segment duration"]
        self.__config["overlap ratio"] = conf["overlap ratio"]

        #Mic stream initialization
        self.__streambits = int(self.__config["sampling rate"] / self.__CHUNKS_PER_SEGMENT)
        #Add silent segment
        silent_chunk = (np.zeros(self.__streambits)).astype(np.float32)
        for i in range(0, int(self.__CHUNKS_PER_SEGMENT * (self.__config["segment duration"] / 1000))):
            self.__chunks.append(silent_chunk)


    def getdevices(self):
        """
        List available audio input devices
        """
        for i in range(0, len(self.__available_devices)):
            logger.debug("Input Device id %i - %s", i, self.__available_devices[i])
    
    def selectdevice(self, id):
        """
        Select audio input device to be used
        """
        if id >= len(self.__available_devices) or id < 0:
            devices = {i: self.__available_devices[i] for i in range(0, len(self.__available_devices))}
            logger.warning(
                "Device with id %i not available, available devices:\n %s", id, pformat(devices)
            )
            return 0
        self.__selected_device_index = id
        self.getselecteddevice()
    
    def getselecteddevice(self):
        """
        Return selected audio input device info
        """
        logger.info(
            "Selected device %i - %s", self.__selected_device_index, self.__available_devices[self.__selected_device_index]
        )
        return {self.__selected_device_index: self.__available_devices[self.__selected_device_index]}
    
    def streamdatacallback(self, data, frame_count, time_info, status):
        self.__chunks.append(data)
        self.__chunks.pop(0)
        self.__CHUNK_COUNTER += 1
        if self.__CHUNK_COUNTER >= int(self.__CHUNKS_PER_SEGMENT * self.__config["overlap ratio"] * (self.__config["segment duration"] / 1000)):
            #Save collected chunks with total duration = config["segment duration"]
            self.__segment.append(np.frombuffer(b''.join(self.__chunks), np.float32))
            logger.info("Audio segment created")

            self.__CHUNK_COUNTER = 0
        return data, pyaudio.paContinue

    def startstream(self):
        """
        Start streaming selected audio input
        """
        logger.info("Initializing streamer")
        self.stream = self.__mic.open(format = FORMAT,
            channels = CHANNELS,
            rate = self.__config["sampling rate"],
            frames_per_buffer = self.__streambits,
            output = False,
            input = True,
            input_device_index = self.__selected_device_index,
            stream_callback = self.streamdatacallback
        )
        logger.info("Starting audio stream")
        self.stream.start_stream()
        logger.info("Stream started using device %i - %s", self.__selected_device_index, self.__available_devices[self.__selected_device_index])

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
        popped_segments, self.__segment = self.__segment, []
        return popped_segments

    def destroy(self):
        self.__mic.terminate()