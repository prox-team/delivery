from flask import Flask
from config import Config
from flask_mongoengine import MongoEngine

app = Flask(__name__)
app.config.from_object(Config)
db = MongoEngine(app)

from views import *
from admin import *

if __name__ == '__main__':
    app.run(host='0.0.0.0')
