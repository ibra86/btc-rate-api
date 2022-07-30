import json
import re

from src.logger import logger


def err_response_factory_helper(e, msg):
    response = e.get_response()

    response.data = json.dumps(msg)
    response.content_type = "application/json"
    logger.error(f'Error: {msg}')

    return response


def email_validation(email):
    regex = r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'
    return bool(re.fullmatch(regex, email))
