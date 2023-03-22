import logging
import json
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
    __baudrate = 9600
    __gps_dump = "gps.dump"
    __serial = serial.Serial(baudrate=__baudrate, timeout=0, rtscts=True)
    __serial_io = io.TextIOWrapper(io.BufferedRWPair(__serial, __serial))
    __location = {
        "lat": None,
        "lng": None
    }

    ready = False

    def __init__(self, conf:Dict):
        """
        Initialize GPS handler
        """
        #Set config
        self.__port = conf["port"]
        self.__baudrate = conf["baudrate"]
        self.__serial.port = self.__port
        self.__serial.baudrate = self.__baudrate

        #Open serial
        self.start()

    def start(self):
        if self.__serial.is_open:
            logger.info("Serial connection already opened.")
            return True
        else:
            try:
                self.__serial.open()
                return True
            except serial.SerialException as e:
                logger.error(e)
                return False

    def stop(self):
        if self.__serial.is_open:
            self.__serial.close()
        else:
            logger.warning("Can't close serial connection, serial isn't connected.")

    def read_serial(self):
        if not self.__serial.is_open:
            self.start()
        
        try:
            line = self.__serial_io.readline()
            msg = pynmea2.parse(line)
            self.__location = {
                "lat": float(msg.latitude),
                "lng": float(msg.longitude)
            }
            if not self.ready:
                self.ready = True

            with open(self.__gps_dump, 'w') as f:
                f.write(json.dumps({
                    "location": self.__location
                }))

        except pynmea2.ParseError as parse_serial_err:
            logger.error("Invalid GPS serial data : %s", parse_serial_err)
            self.read_dumped_gps_data()
        
        except AttributeError as  invalid_parsed_data_err:
            logger.error("Invalid parsed GPS data\nData: {}".format(msg))
            self.read_dumped_gps_data()
        
        except TypeError as invalid_parsed_data_err:
            logger.error("Invalid parsed GPS data\nParsed Data:\n\tlat: {}, {}\n\t{}, {}".format(msg.latitude, type(msg.latitude), msg.longitude, type(msg.longitude)))
            self.read_dumped_gps_data()

    def read_dumped_gps_data(self):
        try:
            logger.info("Reading dumped gps data at %s", self.__gps_dump)

            with open(self.__gps_dump, 'r') as f:
                self.__location = json.loads(f.read())["location"]

            if not self.ready:
                self.ready = True
            
        except FileNotFoundError as no_file_err:
            logger.error("No gps dump data\nDevice didn't get any GPS signal or other undiagnosed error\nDetection result won't be sent to the server")

    def get_lat_lng(self):
        return self.__location