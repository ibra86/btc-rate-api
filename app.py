import json

from flask import Flask, request, jsonify, render_template
from flask_mail import Mail, Message
from werkzeug.exceptions import HTTPException, Conflict

from src.clients.api_call import get_msg_rate
from src.clients.registry import EmailRegistry
from src.config.flask_config import FlaskConfig
from src.helpers import err_response_factory_helper
from src.logger import logger

app = Flask(__name__)

app.config.from_object(FlaskConfig)

mail = Mail(app)

email_registry = EmailRegistry()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/rate', defaults={'currency_from': 'BTC', 'currency_to': 'UAH'})
@app.route('/api/rate/<currency_from>/<currency_to>')
def get_rate(currency_from, currency_to):
    # TODO:
    # api = ClientAPI()
    # msg = api.get_msg(currency_from, currency_to)
    msg = get_msg_rate(currency_from, currency_to)
    return jsonify(msg)


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


@app.route('/api/sendEmails', defaults={'currency_from': 'BTC', 'currency_to': 'UAH'}, methods=['POST'])
@app.route('/api/sendEmails/<currency_from>/<currency_to>', methods=['POST'])
def send_emails(currency_from, currency_to):
    # msg = get_msg_rate(currency_from, currency_to)
    msg = {"description": "exchange rate", "currency_from": "BTC", "currency_to": "UAH", "rate": 887743.141032,
           "timestamp": "2022-07-30 15:16:03", "status": "success"}
    m = Message(subject=f'Rate for {currency_from}/{currency_to}',
                body=json.dumps(msg, indent=4),
                sender=app.config['MAIL_USERNAME'],
                recipients=email_registry.emails)
    mail.send(m)
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
