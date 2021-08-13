from flask import Flask, render_template, Markup, url_for
from flask import request, redirect, session
from auth import LoginForm
from registration import RegisterForm
from dbusers import UserModel, DB
from werkzeug.utils import secure_filename
import smtplib
import os
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'contacts'



@app.route('/')
@app.route('/index/')
def search():
    if 'username' not in session:
        return redirect('/auth')
    roots = ""
    if session["user_id"] == 1:
        roots = "студент"
    if session["user_id"] == 2:
        roots = "преподаватель"
    return render_template('search.html', roots=roots, name=session['username'])


@app.route('/auth', methods=['POST', 'GET'])
def auth():
    form=LoginForm()
    if form.validate_on_submit():
        mail = form.mail.data
        password = form.password.data

        if((('@dvfu.ru' in str(mail)) == False) and ((('@students.dvfu.ru' in str(mail))) == False)):
            return render_template('auth.html', form=form, errorauth=str(mail))

        db = DB()

        if("@dvfu.ru" in mail):

            user_model = UserModel(db.get_connection())
            exists = user_model.exists(mail, password)

        if("@students.dvfu.ru" in mail):
            user_model = UserModel(db.get_connection())
            exists = user_model.exists(mail, password)

        if (exists[0]):
            session['username'] = user_model.get(mail)[0]
            session['user_id'] = user_model.get(mail)[1]
            return redirect("/index")
        else:
            return render_template('auth.html', form=form, errorauth='не зарегистрированный пользователь')
    return render_template('auth.html', form=form, errorauth='')


@app.route("/registration", methods=["GET", "POST"])
def reg():
    def random_id(length):
        number = '0123456789'
        alpha = 'abcdefghijklmnopqrstuvwxyz'
        id = ''
        for i in range(0, length-1, 2):
            id += random.choice(number)
            id += random.choice(alpha)
        return id
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        mail = form.mail.data
        unicid = random_id(5)

        db = DB()
        if((('@dvfu.ru' in str(mail)) == False) and ((('@students.dvfu.ru' in str(mail))) == False)):
            return render_template('auth.html', form=form, error_reg="для входа используйте Ваш адрес корпоративной почты")
        if("@students.dvfu.ru" in mail):
            access = 1
            user_model= UserModel(db.get_connection())
            cls = form.clas.data
        if("@dvfu.ru" in mail):
            access = 2
            user_model = UserModel(db.get_connection())
            cls=""
        check = user_model.check(mail)
        if (check[0]):
            return render_template('registration.html', error_reg="пользователь существует", form=form)
        else:
            user_model.insert(username, password, mail, cls, unicid, access)
            smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
            smtpObj.starttls()
            smtpObj.login('contactsuniver@gmail.com', 'somePas1')
            msg = f'From: <contactsuniver@gmail.com>\n' \
                      f'To: <{mail}>\n' \
                      f'Subject: confirm\n\n' \
                      f'http://46.46.5.24/confirm/{unicid}'
            smtpObj.sendmail("contactsuniver@gmail.com", mail, msg)
            smtpObj.quit()
            #user_model.updatestatus(unicid)

            return render_template('registration.html',
                                   error_reg="для завершения регистрации перейдите на ссылку отправленную на ваш почтовый адресс",
                                   form=form)
    return render_template('registration.html', error_reg="", form=form)

@app.route("/confirm/<unicid>")
def confirm(unicid):
    db = DB()
    user_model = UserModel(db.get_connection())
    user_model.updatestatus(unicid)
    return redirect("/auth")

@app.route('/logout')
def logout():
    session.pop('username',0)
    session.pop('user_id',0)
    return redirect("/index")

if __name__ == '__main__':
    app.run(port=80, host='0.0.0.0', debug=True)



