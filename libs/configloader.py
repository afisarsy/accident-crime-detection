import logging
import json

logger = logging.getLogger(__name__)

config = dict()
configFile = "config.file"

try:
    with open(configFile, 'r') as file:
	    config = json.loads(file.read())
except:
    logger.error(
        "Error loading config file. "
    )