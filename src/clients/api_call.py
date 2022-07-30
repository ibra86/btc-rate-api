import os
from datetime import datetime as dt

import requests

CONVERSION_RATE_API_URL = 'https://api.apilayer.com/exchangerates_data/convert'
API_KEY = os.environ['api_key']


def get_rate_api_call(currency_from, currency_to):
    resp = requests.get(url=CONVERSION_RATE_API_URL,
                        params={'from': currency_from, 'to': currency_to, 'amount': 1},
                        headers={"apikey": API_KEY})
    data = resp.json().get('info')
    return data


def get_msg_rate(currency_from, currency_to):
    data = get_rate_api_call(currency_from, currency_to)
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
