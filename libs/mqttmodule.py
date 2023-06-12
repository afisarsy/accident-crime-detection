import logging
import json
from typing import Dict

from libs.deviceinfo import device

import paho.mqtt.client as mqtt

logger = logging.getLogger(__name__)

class MQTT:
    """
    MQTT Communication Object
    """

    def __init__(self, conf:Dict = {}):
        """
        Initalize communication through MQTT
        """
        #config
        self.__host = "host"
        self.__port = 1883
        self.__subscribe_topics = []
        self.connected = False
        
        #Set config if provided
        if "host" in conf.keys():
            self.__host = conf["host"]
        if "port" in conf.keys():
            self.__port = conf["port"]
        if "subscribe_topics" in conf.keys():
            self.__subscribe_topics = conf["subscribe_topics"]
        if "id" in conf.keys():
            self.device_id = conf['device_id']
        else:
            self.device_id = device.getid()

        #Initialize MQTT
        self.__init_mqtt()
    
    def __init_mqtt(self):
        self.__client = mqtt.Client(client_id=self.device_id)
        self.__client.on_connect = self.__mqtt_on_connect
        self.__client.on_disconnect = self.__mqtt_on_disconnect
        self.__client.on_message = self.__mqtt_on_message
        self.__client.reconnect_delay_set(min_delay=1, max_delay=120)
        self.__client.connect_async(host=self.__host, port=self.__port)
        self.__client.loop_start()
    
    def __mqtt_on_connect(self, client, userdata, flags, rc):
        self.connected = True
        logger.info("MQTT Client Connected")

        for topic in self.__subscribe_topics:
            self.__client.subscribe(topic)
    
    def __mqtt_on_disconnect(self, client, userdata, rc):
        self.connected = False
        logger.info("MQTT Client Disconnected")
    
    def __mqtt_on_message(self, client, userdata, msg):
        topic = msg.topic
        payload = msg.payload.decode("utf-8")
        logger.debug("Message from topic : %s\nPayload : %s".format(topic, payload))

    def stopmqtt(self):
        self.__client.disconnect()
        self.__client.loop_stop()

    def publishdata(self, topic, data):
        self.__client.publish(topic + device.getid(), json.dumps(data))