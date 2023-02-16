import logging
from pprint import pformat
from datetime import datetime
import sys

import numpy as np
import pyaudio

logger = logging.getLogger(__name__)

FORMAT=pyaudio.paInt16
CHANNELS = 1

class Mic:
    """
    Microphone Object
    """
    
    #config
    __sampling_rate = 44100
    __segment_duration = None
    __overlap_ratio = None

    #mic device params
    __mic = None
    __selected_device_index = 0
    __available_devices = {}

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
        self.__available_devices = Mic.getdevices()

        #Load scheme
        self.__sampling_rate = conf["sampling rate"]
        self.__segment_duration = conf["segment duration"]
        self.__overlap_ratio = conf["overlap ratio"]

        #Mic stream initialization
        self.__streambits = int(self.__sampling_rate / self.__CHUNKS_PER_SEGMENT)
        #Add silent segment
        silent_chunk = (np.zeros(self.__streambits)).astype(np.int16)
        for i in range(0, int(self.__CHUNKS_PER_SEGMENT * (self.__segment_duration / 1000))):
            self.__chunks.append(silent_chunk)

    @staticmethod
    def getdevices():
        """
        List available audio input devices
        """
        mic = pyaudio.PyAudio()
        info = mic.get_host_api_info_by_index(0)
        all_devices = info.get('deviceCount')
        mics = {}
        for i in range(0, all_devices): # type: ignore
            if (mic.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 1: # type: ignore
                mics[str(mic.get_device_info_by_host_api_device_index(0, i).get('index'))] = mic.get_device_info_by_host_api_device_index(0, i).get('name')
        return mics
    
    def selectdevice(self, id):
        """
        Select audio input device to be used
        """
        if str(id) not in self.__available_devices.keys():
            logger.error(
                "Device with id %i not available\nAvailable audio input : \n %s", id, pformat(self.__available_devices)
            )
            sys.exit(0)
        self.__selected_device_index = id
        self.getselecteddevice()
    
    def getselecteddevice(self):
        """
        Return selected audio input device info
        """
        logger.info(
            "Selected device %i - %s", self.__selected_device_index, self.__available_devices[str(self.__selected_device_index)]
        )
        return {self.__selected_device_index: self.__available_devices[str(self.__selected_device_index)]}
    
    def streamdatacallback(self, data, frame_count, time_info, status):
        self.__chunks.append(data)
        self.__chunks.pop(0)
        self.__CHUNK_COUNTER += 1
        if self.__CHUNK_COUNTER >= int(self.__CHUNKS_PER_SEGMENT * self.__overlap_ratio * (self.__segment_duration / 1000)): # type: ignore
            #Save collected chunks with total duration = config["segment duration"]
            segment_data = {
                "segment" : np.frombuffer(b''.join(self.__chunks), np.int16).astype(np.float32),
                "time" : datetime.now()
            }
            self.__segment.append(segment_data)
            
            logger.debug("Audio segment created")

            self.__CHUNK_COUNTER = 0
        return data, pyaudio.paContinue

    def startstream(self):
        """
        Start streaming selected audio input
        """
        logger.info("Initializing streamer")
        self.stream = self.__mic.open(format = FORMAT, # type: ignore
            channels = CHANNELS,
            rate = self.__sampling_rate,
            frames_per_buffer = self.__streambits, # type: ignore
            output = False,
            input = True,
            input_device_index = self.__selected_device_index,
            stream_callback = self.streamdatacallback
        )
        logger.info("Starting audio stream")
        self.stream.start_stream()
        logger.info("Stream started using device %i - %s", self.__selected_device_index, self.__available_devices[str(self.__selected_device_index)])

    def stopstream(self):
        """
        Stop audio input stream
        """
        #stop audio input stream
        logger.info("Stopping stream")
        self.stream.stop_stream() # type: ignore
        self.stream.close() # type: ignore
        logger.info("Stream stopped")
    
    def popallsegments(self):
        """
        Pop all available segments
        """
        popped_segments, self.__segment = self.__segment, []
        return popped_segments

    def destroy(self):
        self.__mic.terminate() # type: ignore