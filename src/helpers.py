import json

from src.logger import logger


def err_response_factory_helper(e, msg):
    response = e.get_response()

    response.data = json.dumps(msg)
    response.content_type = "application/json"
    logger.error(f'Error: {msg}')

    return response
