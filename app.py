from datetime import datetime as dt

from flask import Flask, request, jsonify, render_template
from werkzeug.exceptions import HTTPException, Conflict

from src.clients.api_call import get_rate_api_call
from src.clients.registry import EmailRegistry
from src.helpers import err_response_factory_helper
from src.logger import logger

app = Flask(__name__)

app.config["JSON_SORT_KEYS"] = False

email_registry = EmailRegistry()


@app.route('/')
def get_root():
    return render_template('index.html')


@app.route('/api/rate', defaults={'currency_from': 'BTC', 'currency_to': 'UAH'})
@app.route('/api/rate/<currency_from>/<currency_to>')
def get_rate(currency_from, currency_to):
    data = get_rate_api_call(currency_from, currency_to)
    rate = data.get('rate')
    timestamp = data.get('timestamp')
    res = {
        "description": "exchange rate",
        "currency_from": f"{currency_from}",
        "currency_to": f"{currency_to}",
        "rate": rate,
        "timestamp": f"{dt.fromtimestamp(timestamp)}",
        "status": "success"
    }
    return jsonify(res)


@app.route('/api/subscribe', methods=['POST'])
def subscribe():
    email = request.form.get('email')
    emails = email_registry.emails
    if email not in emails:
        email_registry.add(email)
        res = {
            "data": {
                "email": email
            },
            "message": "email is added to subscription",
            "status": "success"
        }
        logger.info(res)
        return jsonify(res)
    raise Conflict(email)


@app.route('/api/sendEmails', methods=['POST'])
def send_emails():
    return jsonify(todo=True)


@app.errorhandler(Conflict)
def handle_conflict_exception(e):
    msg = {
        "data": {
            "email": str(e.description)
        },
        "message": "email is already subscribed",
        "status": "fail"
    }
    response = err_response_factory_helper(e, msg)
    return response


@app.errorhandler(HTTPException)
def handle_http_exception(e):
    msg = {
        "code": e.code,
        "name": e.name,
        "description": str(e.description),
    }
    response = err_response_factory_helper(e, msg)
    return response
