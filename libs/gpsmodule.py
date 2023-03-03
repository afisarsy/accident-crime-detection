import logging
from typing import Dict
import io

import serial
import pynmea2

logger = logging.getLogger(__name__)

class GPS:
    """
    GPS Object
    """

    #config
    __port = ""
    __baud_rate = 19200
    __serial = None
    __serial_io = None
    __location = {
        "lat": 1.32131331,
        "lng": 0.42131312
    }

    def __init__(self, conf:Dict):
        """
        Initialize GPS handler
        """
        #Set config
        self.__port = conf["port"]
        self.__baud_rate = conf["baud rate"]

        self.__serial = serial.Serial(port=self.__port, baudrate=self.__baud_rate, rtscts=1)
        self.__serial_io = io.TextIOWrapper(io.BufferedRWPair(self.__serial, self.__serial))

    def start(self):
        if self.__serial is None:
            logger.info("Failed to create Serial object")
        elif self.__serial.is_open():
            logger.warning("Serial connection already opened.")
        else:
            self.__serial = serial.Serial(self.__port)

    def stop(self):
        if self.__serial is not None and self.__serial.is_open():
            self.__serial.close()
        else:
            logger.warning("Can't close serial connection, serial isn't connected.")

    def read_serial(self):
        line = self.__serial_io.readline()
        msg = pynmea2.parse(line)
        self.__location = {
            "lat": msg.latitude,
            "lng": msg.longitude
        }

    def get_lat_lng(self):
        return self.__location