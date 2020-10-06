import secrets
import os

class Config:
    SECRET_KEY = secrets.token_urlsafe(32)
    MONGODB_HOST = 'mongodb'
    MONGODB_DB = 'delivery'
    FLASK_DEBUG = False
    FIRST_RUN = False
    CAPTCHA_SERVER_KEY = '6LctT7wZAAAAABHdfuFF2PMUljFyZfC3Ai6_FKND'  # google recaptcha
    CAPTCHA_CLIENT_KEY = '6LctT7wZAAAAAEuScMNpqsw9zXnNUMLvY_lq9_Xr' # google recaptcha
    PASSWORD = 'superVeryLongAdminPassword'

