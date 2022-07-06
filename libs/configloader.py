import logging
import json

logger = logging.getLogger(__name__)

def loadconfig(model_path):
    config = dict()
    config_file = "config.file"
    config_path = model_path[:model_path.rfind("/")+1] + config_file

    try:
        with open(config_path, 'r') as file:
            config = json.loads(file.read())
    except:
        logger.error(
            "Error loading config file in %s", config_path
        )

    return config