import os

import requests

CONVERSION_RATE_API_URL = 'https://api.apilayer.com/exchangerates_data/convert'
API_KEY = os.environ['api_key']


def get_rate_api_call(currency_from, currency_to):
    resp = requests.get(url=CONVERSION_RATE_API_URL,
                        params={'from': currency_from, 'to': currency_to, 'amount': 1},
                        headers={"apikey": API_KEY})
    data = resp.json().get('info')
    return data
