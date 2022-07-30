import logging

from src.constants import SERVICE_NAME

logging.basicConfig()
logger = logging.getLogger(SERVICE_NAME)
logger.setLevel(logging.DEBUG)
