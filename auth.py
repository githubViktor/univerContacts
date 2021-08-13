from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField, PasswordField, BooleanField, SubmitField
import sys
import urllib3


class LoginForm(FlaskForm):
    mail = StringField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    #remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')
