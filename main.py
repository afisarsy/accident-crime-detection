import logging
from pprint import pformat
import asyncio

from mainparser import parser
from libs.logger import initlogger
from libs.deviceinfo import device

logger = logging.getLogger(__name__)
loop = asyncio.get_event_loop()

def main():
    """
    Audio-based detection and crime detection system
    Realtime runtime system
    """

    options = parser.parse_known_args()[0]
    initlogger(options.log)

    if str.lower(options.mode) == "run":
        running()
    elif str.lower(options.mode) == "get":
        getparam()
    elif str.lower(options.mode) == "test":
        test()


def running():
    """
    Run accident and Crime Detection System
    """
    options = parser.parse_args()

    #MQTT config
    mqtt_config = {
        "host": "103.106.72.182",
        "port": 1887
    }
    mqtt_topics = {
        "data": "acd/node/",
        "test": "acd/test/"
    }
    
    #Model Initialization
    from libs.configmodule import loadconfig
    from libs.nnmodule import NN, Rot90
    
    options.model = options.model.replace("\\","/")

    model_config = loadconfig(options.model)
    custom_objects = {"Rot90" : Rot90}

    logger.info("Using model %s", options.model)
    logger.info("Loading Config File\nConfig : \n%s",pformat(model_config))

    #Initialize gps module
    from libs.gpsmodule import GPS

    #gps config
    gps_config = {
        "port": "",
        "baudrate": 9600
    }
    if device.getname() == "Raspberry Pi":
        gps_config["port"] = "/dev/ttyS0"
    elif device.getname() == "Jetson Nano":
        gps_config["port"] = "/dev/ttyTHS1"
    elif device.getname() == "Windows PC":
        gps_config["port"] = "COM8"
    else:
        gps_config["port"] = "/dev/ttyACM0"
        
    gps = GPS(gps_config)

    #mic initialization
    from libs.michandler import Mic
    mic = Mic(model_config)
    mic.selectdevice(options.mic)
    mic.getselecteddevice()
    #start audio stream
    mic.startstream()

    #Output mapper
    output_map = {
        "conversation" : "normal",
        "engine_idling" : "normal",
        "rain" : "normal",
        "road_traffic" : "normal",
        "thunderstorm" : "normal",
        "wind" : "normal",
        "car_crash" : "accident",
        "gun_shot" : "crime",
        "jambret" : "crime",
        "maling" : "crime",
        "rampok" : "crime",
        "scream" : "crime",
        "tolong" : "crime"
    }

    #NN initialization
    nn = NN(options.model, custom_objects, output_map, model_config)

    #tasks declaration
    from maintasks import featureextreaction, detection, gpsread
    tasks = asyncio.gather(
        loop.create_task(featureextreaction(options, mic.popallsegments, mic.stream.is_active, nn, model_config, "Tests/save_spectrogram/spectrogram")),
        loop.create_task(gpsread(gps, mic.stream.is_active)),
        loop.create_task(detection(options, mic.stream.is_active, nn, options.threshold, model_config, gps.get_lat_lng, mqtt_config, mqtt_topic=mqtt_topics["test"]))
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
        #loop.close()


def getparam():
    """
    Get available params
    """
    #Load required Libraries
    from libs.michandler import Mic

    options = parser.parse_args()

    if options.param == "mic":
        available_devices = Mic.getdevices()
        logger.info("Get I/O Devices\nAvailable audio input : \n%s", pformat(available_devices))
    elif options.param == "id":
        logger.info("Get Device ID\nDevice ID : %s", device.getid())


def test():
    """
    Run unit test
    """

    options = parser.parse_args()

    if options.test_mode == "mqtt":
        from maintests import testmqtt
        testmqtt(options)
    elif options.test_mode == "gps":
        from maintests import testgps
        testgps(options)
    elif options.test_mode == "inferrt":
        from maintests import testinferreal
        options.no_mqtt = True
        options.log_process = True
        testinferreal(options)
    elif options.test_mode == "infer":
        from maintests import testinfer
        testinfer(options)

if __name__ == '__main__':
    main()