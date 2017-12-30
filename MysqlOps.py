import os, time
from flask_mysqldb import MySQL

mysql = MySQL()

"""
insert_sql = [
    "INSERT INTO `user` (username, fullname, password,email) VALUES('tugce123', 'Tugce Cetinkaya'  ,'12345','tugce@gmail.com');",
    "INSERT INTO `user` (username, fullname, password,email) VALUES('ergin123', 'Ergin Cetinhafif' ,'12345','ergin@gmail.com');",
    "INSERT INTO `user` (username, fullname, password,email) VALUES('ceo123'  , 'Ceo Cetin'        ,'12345','ceo@gmail.com');",
]
"""
def init(app):
    """
        mysql bilgilerini .env uzantili dosyanini icine yerlestiriyoruz.
        'dotenv' ile mysql bilgilerini cekerek
        buradan  gerekli bagalntilari sagliyoruz.
    """
    app.config['MYSQL_USER'] = os.environ.get("MYSQL_USER")
    app.config['MYSQL_PASSWORD'] = os.environ.get("MYSQL_PASSWORD")
    app.config['MYSQL_DB'] = os.environ.get("MYSQL_DB")
    app.config['MYSQL_HOST'] = os.environ.get("MYSQL_HOST")
    mysql.init_app(app)
    return app

def get_time():
    return time.strftime("%Y-%m-%d-%H-%M-%S")

def create_filename(username, date, extension):
    return username + "_" + date + extension

def create_tables():
    general_sql = """
    DROP TABLE IF EXISTS `photo`;
    DROP TABLE IF EXISTS `user`;
    CREATE TABLE `user` (
    `userid` int(11) NOT NULL AUTO_INCREMENT,
    `username` varchar(100) DEFAULT NULL UNIQUE,
    `fullname` varchar(100) DEFAULT NULL,
    `password` varchar(100) DEFAULT NULL,
    `email` varchar(100) DEFAULT NULL UNIQUE,
    PRIMARY KEY (`userid`)
    ) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;

    CREATE TABLE `photo` (
    `photoid` int(11) NOT NULL AUTO_INCREMENT,
    `username` varchar(100) NOT NULL,
    `date` varchar(100) NOT NULL,
    `filename` varchar(100) NOT NULL,
    PRIMARY KEY (`photoid`),
    FOREIGN KEY (username) REFERENCES user(username) ON DELETE CASCADE
    ) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;
    """
    cur = mysql.connection.cursor()
    cur.execute(general_sql)
    data = cur.fetchall()
    return data, None

def insert_user(username, fullname, password, email):
    try:
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO `user` (username, fullname, password,email) VALUES(%s,%s,%s,%s)",
                    (username, fullname, password, email))
        mysql.connection.commit()
        return "", None # No problem
    except Exception as e:
        print(e)
        return "", e    # Yes, we have problem

def insert_photo(username, realphotoname):
    date = get_time()
    extension = os.path.splitext(realphotoname)[1]
    filename = create_filename(username, date, extension)
    print(date, extension, filename)
    try:
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO `photo` (username, date, filename) VALUES(%s,%s, %s)",
                    (username, date, filename))
        mysql.connection.commit()
        return filename, None # No problem
    except Exception as e:
        print(e)
        return "", e    # Yes, we have problem

def get_users():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM `user`")
        users_info = cur.fetchall()
        return users_info, None # No problem
    except Exception as e:
        print(e)
        return "", e    # Yes, we have problem

def get_version():
    try:
        cur = mysql.connection.cursor()
        cur.execute("select version();")
        data = cur.fetchall()
        return data, None # No problem
    except Exception as e:
        print(e)
        return "", e    # Yes, we have problem

def get_user_information_by_username(username):
    user_info = {}  # dict()
    # Burda username ile mysql den data aliriz, ve istek atana json formatin da gondeririz.
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM `user` WHERE `username` = '{}';".format(username))
        row = cur.fetchone()
        user_info['userid'] = row[0]
        user_info['username'] = row[1]
        user_info['fullname'] = row[2]
        user_info['password'] = row[3]
        user_info['email'] = row[4]
        user_info['pics'] = []
        return user_info, None
    except Exception as e:
        print(e)  # (1026, 'email or username is not unique')
        return "", str(e.args[1])

def update_user_information_by_username(currentusername, data):
    try:
        cur = mysql.connection.cursor()
        cur.execute(
            "UPDATE `user` SET `username`='{1}', `fullname`='{2}', `password`='{3}', `email`='{4}' WHERE `username`='{0}'".format(
                currentusername, data['username'], data['fullname'], data['password'], data['email']))
        mysql.connection.commit()
        return data, None
    except Exception as e:
        print(e)
        return "", e
  
def delete_user_by_username(username):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM `user` WHERE `username`='{0}'".format(username))
        mysql.connection.commit()
        return "", None
    except Exception as e:
        print(e)
        return "", e

def get_user_pics_by_username(username):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT `filename` FROM `photo` WHERE `username`='{0}'".format(username))
        pics = cur.fetchall()
        return pics, None # No problem
    except Exception as e:
        print(e)
        return "", e    # Yes, we have problem

def is_photo_exists(photoname):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM `photo` WHERE `filename`='{0}'".format(photoname))
        result = cur.fetchall()
        if result:
            return True
        return False
    except Exception as e:
        print(e)
        return False

def get_photonames():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT `filename` FROM `photo`")
        photonames = cur.fetchall()
        return photonames, None # No problem
    except Exception as e:
        print(e)
        return "", e    # Yes, we have problem

def check_email_password(email, password):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT username FROM `user` WHERE `email` = '{}' AND `password` = '{}';".format(email, password))
        row = cur.fetchone()
        print(row)
        if row is None:
            return "", "Not correct email or password"
        username = row[0]
        return username, None
    except Exception as e:
        print(e)
        return "", str(e.args[1])

def login(email, password):
    username, err = check_email_password(email, password)
    if err is None:
        result, err = get_user_information_by_username(username)
        if err is None:
            return result, None

    return "", err
