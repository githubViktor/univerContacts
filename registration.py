from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, ValidationError
from wtforms import StringField, PasswordField, BooleanField, SubmitField
import sys
import urllib3


class RegisterForm(FlaskForm):
    username = StringField('Введите фио', validators=[DataRequired()])
    password = PasswordField('Введите пароль', validators=[DataRequired()])
    mail = StringField('Введите mail', validators=[DataRequired()])
    clas = StringField('Введите свою группу ', validators=[DataRequired()])
    submit = SubmitField('Регистрация')
    def student(self, field):
        if("@students.dvfu.ru" in str(field.data)):
            return True;
    def notvery(self, field):
        if(("@dvfu.ru" in str(field.data)) == False and ("@students.dvfu.ru" in str(field.data)) == False):
           return True
