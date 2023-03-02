from statistics import mean
from typing import Dict
import math
from unittest import result

R = 6378.137

class DataHandler:
    """
    Data Handler class
    """
    __initial_data = {
        "status": "",
        "lat": 2,
        "lng": 2
    }
    __data = []
    __min_length = 3
    __gps_tollerance = 10 #in meters
    __last_data = __initial_data
    __last_valid_status = ""
    __callibration_cycle_total = 5
    __callibration_cycle_index = 0

    def __init__(self, conf:Dict = {}):
        """
        Output data handler object
        """
        #Set config if provided
        if all(param in conf.keys() for param in ["segment duration", "overlap ratio", "min duration"]):
            self.__min_length = math.ceil((conf["min duration"] * 1000.) / (conf["segment duration"] * conf["overlap ratio"]))
        if "gps tollerance" in conf.keys():
            self.__gps_tollerance = conf["gps tollerance"]
        if "callibration cylce" in conf.keys():
            self.__callibration_cycle_total = conf["callibration cylce"]
        if "min length" in conf.keys():
            self.__min_length = conf["min length"]
    
    def submit(self, new_data):
        """
        Return True if the data persist for specified duration or gps data changed.
        """
        is_new = False
        #Analyze data
        if new_data["status"] == self.__last_data["status"]:
            self.__data.append(new_data)
            if len(self.__data) > self.__min_length + 1:
                self.__data.pop(0)
        else:
            self.__data = [new_data]
        
        #Ignore the first data (Callibration)
        if self.__callibration_cycle_index < self.__callibration_cycle_total:
            self.__callibration_cycle_index += 1
        else:
            #Get data gps mean location
            mean_loc = {
                "lat": mean([data["lat"] for data in self.__data]),
                "lng": mean([data["lng"] for data in self.__data])
            }
            #Status persist for specified duration or gps moved beyond gps tollerance distance
            if (len(self.__data) == self.__min_length and new_data["status"] != self.__last_valid_status) or DataHandler.gps_get_distance(mean_loc, new_data) > self.__gps_tollerance:
                self.__last_valid_status = new_data["status"]
                is_new = True

        #Update last data
        self.__last_data = new_data

        return is_new

    @staticmethod
    def gps_get_distance(loc_1, loc_2):
        """
        Measure 2 gps location in meters
        """
        dist_lat = (loc_2["lat"] * math.pi / 180) - (loc_1["lat"] * math.pi / 180)
        dist_lng = (loc_2["lng"] * math.pi / 180) - (loc_1["lng"] * math.pi / 180)
        a = math.sin(dist_lat / 2) * math.sin(dist_lat / 2) + math.cos(loc_1["lat"] * math.pi / 180) * math.cos(loc_2["lat"] * math.pi / 180) * math.sin(dist_lng / 2) * math.sin(dist_lng / 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        d = R * c
        return d * 1000 #Convert to meters