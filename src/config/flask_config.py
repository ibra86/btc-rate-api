import os


class FlaskConfig:
    JSON_SORT_KEYS = False
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = os.environ['email_user']
    MAIL_PASSWORD = os.environ['email_pass']
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
