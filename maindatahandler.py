from statistics import mean
from typing import Dict
import math
from unittest import result

R = 6378.137

class DataHandler:
    """
    Data Handler class
    """
    __INITIAL_DATA = dict({
        "status": "",
        "lat": 91,      #Outside Lat range (-90 - +90)
        "lng": 181      #Outside Lng range (-180 - +180)
    })

    def __init__(self, conf:Dict = {}):
        """
        Output data handler object
        """
        #Initial params
        self.__data = []
        self.__min_length = 3
        self.__gps_tollerance = 10 #in meters
        self.__last_data = DataHandler.__INITIAL_DATA
        self.__last_valid_status = ""
        self.__callibration_cycle_total = 5
        self.__callibration_cycle_index = 0

        #Set config if provided
        if all(param in conf.keys() for param in ["segment duration", "overlap ratio", "min duration"]):
            self.__min_length = max(math.ceil((conf["min duration"] * 1000.) / (conf["segment duration"] * conf["overlap ratio"])) - 1, 1)
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
        #Replace gps data with previous value if invalid
        if "lat" in new_data and type(new_data["lat"]) is not float:
            new_data["lat"] = self.__last_data["lat"]
        if "lng" in new_data and type(new_data["lng"]) is not float:
            new_data["lng"] = self.__last_data["lng"]

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
            if "lat" in new_data and "lng" in new_data:
                mean_loc = {
                    "lat": mean([data["lat"] for data in self.__data]),
                    "lng": mean([data["lng"] for data in self.__data])
                }
                distance = DataHandler.gps_get_distance(mean_loc, new_data)
            else:
                distance = 0.

            #Status persist for specified duration or gps moved beyond gps tollerance distance
            if (len(self.__data) == self.__min_length and new_data["status"] != self.__last_valid_status) or distance > self.__gps_tollerance:
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