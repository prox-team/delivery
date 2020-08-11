from flask import Flask, url_for
from flask_wtf.csrf import CSRFProtect
from config import Config
from models import *
from flask_migrate import Migrate
from csv_to_db import update


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    migrate = Migrate(app, db)
    db.init_app(app)
    if Config.FIRST_RUN:
        with app.app_context():
            update()
    return app


app = create_app()

from views import *
from admin import *

if __name__ == '__main__':
    app.run(debug=True)
