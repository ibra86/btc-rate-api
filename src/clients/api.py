from datetime import datetime as dt
from http.client import HTTPException

import requests

from src.config.config import CONFIG
from src.logger import logger
from abc import ABC, abstractmethod

config_api = CONFIG.get_config('api')


class API(ABC):
    @abstractmethod
    def get_msg(self, *args, **kwargs):
        pass


class CurrencyRateAPI:

    @staticmethod
    def get_rate_api_call(currency_from, currency_to):
        try:
            resp = requests.get(url=config_api['url'],
                                params={'from': currency_from, 'to': currency_to, 'amount': 1},
                                headers={"apikey": config_api['api_key']})
            data = resp.json().get('info')
            return data
        except Exception as e:  # noqa
            logger.error(f'Error: accessing the 3rd party API on {config_api["url"]} - {e}')
            return {}

    def get_msg(self, currency_from, currency_to):
        data = self.get_rate_api_call(currency_from, currency_to)
        if data:
            rate = data.get('rate')
            timestamp = data.get('timestamp')
            msg = {
                "description": "exchange rate",
                "currency_from": f"{currency_from}",
                "currency_to": f"{currency_to}",
                "rate": rate,
                "timestamp": f"{dt.fromtimestamp(timestamp)}",
                "status": "success"
            }
            return msg
        raise HTTPException
