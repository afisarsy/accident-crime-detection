import logging
import json

logger = logging.getLogger(__name__)
extension = ".conf"

def loadconfig(model_path):
    config_file = model_path[:model_path.rfind('.h5')] + extension
    config = dict()
    try:
        with open(config_file) as f:
            config = json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError("File %s not found", config_file)

    return config

def saveconfig(save_path, config):
    try:
        with open(save_path + extension, 'w') as f:
            f.write(json.dumps(config))
    except e:
        logger.error(e)
    logger.info("Configuration saved to %s", save_path + extension)