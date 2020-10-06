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
    CAPTCHA_SERVER_KEY = '6LctT7wZAAAAABHdfuFF2PMUljFyZfC3Ai6_FKND'  # google recaptcha
    CAPTCHA_CLIENT_KEY = '6LctT7wZAAAAAEuScMNpqsw9zXnNUMLvY_lq9_Xr' # google recaptcha
    PASSWORD = 'superVeryLongAdminPassword'
=======
    MONGODB_DB = 'delivery-base'
    MONGODB_USERNAME = 'delivery-user'
    MONGODB_PASSWORD = 'delivery-password'
    FLASK_DEBUG = False
    FIRST_RUN = False
    CAPTCHA_SERVER_KEY = os.environ['CAPTCHA_SERVER_KEY'] # google recaptcha
    CAPTCHA_CLIENT_KEY = os.environ['CAPTCHA_CLIENT_KEY'] # google recaptcha
    PASSWORD = os.environ['PASSWORD']
>>>>>>> c05d498a730dbbff38e92caec50369764ad37f25

