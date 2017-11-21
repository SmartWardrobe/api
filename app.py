import os

# "Flask" paketini kullanmamizin sebebi uygulamayi ayaga kaldirmak icin.
# "request" paketi ise "api" ye gelen isteklerin icindeki datalari almak icin.
# "jsonify" paketi ise "api" ye gelen isteklere json formatinda data gondermek icin.
from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(), override=True)

# Flask uygulamasini instance i olusturulur.


app=Flask(__name__)
mysql=MySQL()
#mysql bilgilerini .env uzantili dosyanini icine yerlestiriyoruz. 'dotenv' ile mysql bilgilerini cekerek
#buradan  gerekli bagalntilari sagliyoruz.
app.config['MYSQL_USER']     = os.environ.get("MYSQL_USER")
app.config['MYSQL_PASSWORD'] = os.environ.get("MYSQL_PASSWORD")
app.config['MYSQL_DB']       = os.environ.get("MYSQL_DB")
app.config['MYSQL_HOST']     = os.environ.get("MYSQL_HOST")
mysql.init_app(app)



@app.route('/')
def index():
    return "Shut up, bitch"

# "/mysql_test" router'ina istek geldiginde api'nin ayakta oldugu anlamak icin kullandik.
@app.route("/mysql_test")
def hello():
    # Burda mysql istek atiyor, ver donun cevap print ediliyor.
    cur = mysql.connection.cursor()
    cur.execute("select version();")
    #mysql.connection.commit()
    data = cur.fetchall()
    print("tugece")
    return "Ayaktayim, yikilmadim. " + str(data)

@app.route("/api/mysql_init")
def init_mysql():
    table_sql="""
    DROP TABLE IF EXISTS `user`;
    CREATE TABLE `user` (
    `userid` int(11) NOT NULL AUTO_INCREMENT,
    `username` varchar(100) DEFAULT NULL UNIQUE,
    `fullname` varchar(100) DEFAULT NULL,
    `password` varchar(100) DEFAULT NULL,
    `email` varchar(100) DEFAULT NULL UNIQUE,
    PRIMARY KEY (`userid`)
    ) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;
    """
    cur = mysql.connection.cursor()
    cur.execute(table_sql)
    data = cur.fetchall()
    print(data)

    """
    insert_sql = [
        "INSERT INTO `user` (username, fullname, password,email) VALUES('tugce123', 'Tugce Cetinkaya'  ,'12345','tugce@gmail.com');",
        "INSERT INTO `user` (username, fullname, password,email) VALUES('ergın123', 'Ergın Cetinhafif' ,'12345','ergin@gmail.com');",
        "INSERT INTO `user` (username, fullname, password,email) VALUES('ceo123'  , 'Ceo Cetin'        ,'12345','ceo@gmail.com');",
    ]
    """

    try:
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO `user` (username, fullname, password,email) VALUES(%s,%s,%s,%s)",('tugce123', 'Tugce Cetinkaya','12345','tugce@gmail.com'))
        mysql.connection.commit()
    except Exception as e:
        print(e)
        return str(e.args[1])

    return "Tablo yeniden olusturuldu."


# Asil Api asagidaki kodlardan sonra basliyor.
# Api'ye istek ya ionic'ten atarsin ya da ayri bir flask uygulamasindan.
# Suanlik ayri flask uygulamasindan "requests" paketiyle post,put,get,delete istegi aticaz.
# Ionic'le test etmek biraz daha ugrastirici suanlik.
# Ve ilerde mysql'de deneme yaparsiniz. Suanlik static kullanim yapin.
# Bir ileri adimda Authorization yapilacak.

# REST API mantigi, CRUD islemlerini methodlarla ayirmak.
# GET       - READ  islemleri
# POST      - CREATE islemleri
# PUT       - UPDATE islemleri
# DELETE    - DELETE islemleri

# "/api/create_user" router'ina json datasi ile birlikte istek atilir.(POST)
@app.route("/api/create_user", methods=["POST"])
def create_user():
    data = request.get_json()           # Json datasi istegin icinden alinir.
    print(data)
    # Burda bu data ile mysql user eklenir, basarisiz ise status degistirilir.
    newuser = {
        "username": data['username'],
        "fullname": data['fullname'],
        "password": data['password'],
        "email": data['email']
    }
    try:
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO `user` (username, fullname, password,email) VALUES(%s,%s,%s,%s)",(newuser['username'], newuser['fullname'], newuser['password'], newuser['email']))
        mysql.connection.commit()
    except Exception as e:
        print(e)
        return jsonify({"status": "error", "content": str(e.args[1]) })

    return jsonify({"status": "okey", "content": "Kayit basarili, User olusturdum."})

# "/api/user/ergin" veya "/api/user/tugce" normal istek atilir(GET). Ve user nin bilgileri istek atilana geri dondurulur.
@app.route("/api/user/<string:username>", methods=["GET"])
def get_user_information(username):
    print("Okunacak username: ", username)
    user_info = {} # dict()
    # Burda username ile mysql den data aliriz, ve istek atana json formatin da gondeririz.
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM `user` WHERE `username` = '{}';".format(username))
        row = cur.fetchone()
        user_info['userid']   =row[0]
        user_info['username'] =row[1]
        user_info['fullname'] =row[2]
        user_info['password'] =row[3]
        user_info['email']    =row[4]

    except Exception as e:
        print(e)                                                        # (1026, 'email or username is not unique')
        return jsonify({"status": "error", "content": str(e.args[1]) }) # 'email or username is not unique'

    return jsonify({"status": "okey", "data": user_info})

# "/api/user/ergin" istek atilir ama istegin icinde json olur. Cunku Update islemi gerceklestiriliyor.
@app.route("/api/user/<string:currentusername>", methods=["PUT"])
def update_user_information(currentusername):
    data = request.get_json()           # Json datasi istegin icinden alinir.
    print(data)
    print("Guncellenecek username: ", currentusername, " Ve degistirilecek data: ", data)
    try:
        cur = mysql.connection.cursor()
        cur.execute("UPDATE `user` SET `username`='{1}', `fullname`='{2}', `password`='{3}', `email`='{4}' WHERE `username`='{0}'".format(currentusername, data['username'], data['fullname'], data['password'], data['email']))
        mysql.connection.commit()
    except Exception as e:
        print(e)
        return jsonify({"status": "error", "content": str(e.args[1]) })

    return jsonify({"status": "okey", "data": data})

# "/api/user/ergin" istek atilir. Ve dlete islemi gerceklesir.
@app.route("/api/user/<string:username>", methods=["DELETE"])
def delete_user(username):
    print("Silinecek username: ", username)
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM `user` WHERE `username`='{0}'".format(username))
        mysql.connection.commit()
    except Exception as e:
        print(e)
        return jsonify({"status": "error", "content": str(e.args[1]) })

    return jsonify({"status": "okey", "content": "fuck off"})

if __name__ == "__main__":
    app.run()
