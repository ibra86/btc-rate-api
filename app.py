import json

from flask import Flask, request, jsonify, render_template
from flask_mail import Mail, Message
from werkzeug.exceptions import HTTPException, Conflict

from src.clients.api import CurrencyRateAPI, config_api
from src.clients.registry import EmailRegistry
from src.config.flask_config import FlaskConfig
from src.helpers import err_response_factory_helper, email_validation
from src.logger import logger

app = Flask(__name__)

app.config.from_object(FlaskConfig)

mail = Mail(app)

email_registry = EmailRegistry()
api = CurrencyRateAPI()


@app.route('/')
def index():
    logger.info('render index')
    return render_template('index.html')


@app.route('/api/rate', defaults={'currency_from': config_api['default_currency_from'],
                                  'currency_to': config_api['default_currency_to']})
@app.route('/api/rate/<currency_from>/<currency_to>')
def get_rate(currency_from, currency_to):
    msg = api.get_msg(currency_from, currency_to)
    logger.info(f'get currency rate: {msg}')
    return jsonify(msg)


@app.route('/api/subscribe', methods=['POST'])
def subscribe():
    email = request.form.get('email')
    if email_validation(email):
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
            logger.info(f'subscribed: {res}')
            return jsonify(res)
        raise Conflict(email)
    raise HTTPException(email)


@app.route('/api/sendEmails', defaults={'currency_from': config_api['default_currency_from'],
                                        'currency_to': config_api['default_currency_to']}, methods=['POST'])
@app.route('/api/sendEmails/<currency_from>/<currency_to>', methods=['POST'])
def send_emails(currency_from, currency_to):
    msg = api.get_msg(currency_from, currency_to)
    # msg = {"description": "exchange rate", "currency_from": "BTC", "currency_to": "UAH", "rate": 887743.141032,
    #        "timestamp": "2022-07-30 15:16:03", "status": "success"}
    m = Message(subject=f'Rate for {currency_from}/{currency_to}',
                body=json.dumps(msg, indent=4),
                sender=app.config['MAIL_USERNAME'],
                recipients=email_registry.emails)
    mail.send(m)
    logger.info(f'sent currency rate to emails: {email_registry.emails}')
    return jsonify(msg_sent=True)


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
