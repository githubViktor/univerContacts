import sqlite3
from dbusers import UserModel, DB

db = DB()
user_model = UserModel(db.get_connection())
username = input()
password = input()
mail = input()
cls = input()
access = int(input())
unicid = input()
user_model.insert(username, password, mail, cls, unicid, access)
list = user_model.get(mail)
for i in list:
    print(i)

