import os

from envyaml import EnvYAML

from src.constants import CONFIG_FILE_NAME
from src.logger import logger


class Config:
    config_path = os.path.join(os.path.dirname(__file__), CONFIG_FILE_NAME)

    def __init__(self):
        logger.debug('init config')
        self.__config = EnvYAML(self.config_path)

    def get_config(self, sect):
        return self.__config[sect]
