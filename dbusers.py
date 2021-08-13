import sqlite3


class DB():
    def __init__(self, conn=0):
        conn = sqlite3.connect('users.db', check_same_thread=False)
        self.conn = conn

    def get_connection(self):
        return self.conn

    def __del__(self):
        self.conn.close()


class UserModel():
    def __init__(self, connection):
        self.connection = connection
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                        (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                         username VARCHAR(150),
                         password_hash VARCHAR(128),
                         mail VARCHAR(100),
                         cls VARCHAR(25),
                         uid VARCHAR(100),
                         access INTEGER,
                         status INTEGER
                         )''')
        cursor.close()
        self.connection.commit()

    def insert(self, username, password_hash, mail, cls, uid, access):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO users 
                      (username, password_hash, mail, cls, uid, access, status) 
                      VALUES (?,?,?,?,?,?,0)''', (username, password_hash, mail, cls, uid, access))
        cursor.close()
        self.connection.commit()

    def exists(self, mail, password_hash):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE mail = ? AND password_hash = ? AND status = 1",
                       (mail, password_hash))
        row = cursor.fetchone()
        return (True, row[0]) if row else (False,)

    def check(self, mail):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE mail = ? AND status = 1",
                       (mail,))
        row = cursor.fetchone()
        return (True, row[0]) if row else (False,)

    def updatestatus(self, uid):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE users SET status = 1 WHERE uid = ?",
                       (uid,))
        cursor.close()
        self.connection.commit()

    def get(self, mail):
        cursor = self.connection.cursor()
        cursor.execute("SELECT username, access FROM users WHERE mail = ?", (str(mail),))
        row = cursor.fetchone()
        return row
