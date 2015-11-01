from flask.ext.wtf import Form, RecaptchaField
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, EqualTo, Email

__author__ = 'Frito'


class LoginForm(Form):
    email = StringField('Email Address', [DataRequired(), Email()])
    password = PasswordField('Password', [DataRequired()])


class RegisterForm(Form):
    name = StringField('NickName', [DataRequired()])
    email = StringField('Email Address', [DataRequired(), Email()])
    password = PasswordField('Password', [DataRequired()])
    confirm = PasswordField('Repeat Password', [DataRequired(), EqualTo('pasword', message='Passwords must match')])
    accept_tos = BooleanField('I accept the TOS', [DataRequired()])
    recaptcha = RecaptchaField()
