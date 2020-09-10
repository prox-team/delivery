from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, EqualTo, Regexp
from flask_wtf.csrf import CSRFProtect
import requests
import json
from delivery import app
from delivery.config import Config

csrf = CSRFProtect(app)


def check_recapcha(response, remoteip):
    return json.loads(requests.post('https://www.google.com/recaptcha/api/siteverify', data=dict(
        secret=Config.CAPTCHA_SERVER_KEY,
        response=response.get('g-recaptcha-response'),
        remoteip=remoteip
    )).text)['success']


class BaseForm(FlaskForm):
    def validate(self):
        success = super(FlaskForm, self).validate()

        if success and 'g-recaptcha-response' in request.form:
            success = check_recapcha(
                request.form,
                request.remote_addr
            )

        return success


class RegistrationForm(BaseForm):
    name = StringField("Имя", validators=[InputRequired()])
    username = StringField("Почта", validators=[InputRequired()])
    password = PasswordField("Пароль", validators=[InputRequired(),
                                                   Length(min=4, message='Пароль должен быть длиннее'),
                                                   EqualTo('confirm', message='Пароли должны совпадать')])
    confirm = PasswordField('Повторите пароль')


class LoginForm(BaseForm):
    username = StringField("Имя", validators=[InputRequired()])
    password = PasswordField("Пароль", validators=[InputRequired()])


class OrderForm(FlaskForm):
    name = StringField("Имя", default=' ', validators=[InputRequired()])
    address = StringField("Адрес", validators=[InputRequired()])
    email = StringField("Почта", default=' ', validators=[InputRequired()])
    phone = StringField('Ваш телефон', validators=[InputRequired(),
                                                   Regexp("^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$",
                                                          message="Неверно указан номер")])
