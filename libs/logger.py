import logging

def initlogger(level):
    FORMAT = '%(asctime)s - %(name)-20s - %(levelname)-8s - %(message)s'
    logging.basicConfig(format=FORMAT, level=level)