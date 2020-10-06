import secrets
import os

class Config:
    SECRET_KEY = secrets.token_urlsafe(32)
    MONGODB_HOST = 'mongodb'
    MONGODB_DB = 'delivery-base'
    MONGODB_USERNAME = 'delivery-user'
    MONGODB_PASSWORD = 'delivery-password'
    FLASK_DEBUG = False
    FIRST_RUN = False
    CAPTCHA_SERVER_KEY = os.environ['CAPTCHA_SERVER_KEY'] # google recaptcha
    CAPTCHA_CLIENT_KEY = os.environ['CAPTCHA_CLIENT_KEY'] # google recaptcha
    PASSWORD = os.environ['PASSWORD']

