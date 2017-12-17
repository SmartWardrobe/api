import os, json
import requests
import pprint
from flask import Flask, request, jsonify, render_template, redirect, url_for, send_from_directory, flash
from flask_mysqldb import MySQL
from dotenv import load_dotenv, find_dotenv
from werkzeug.utils import secure_filename
# "Flask" paketini kullanmamizin sebebi uygulamayi ayaga kaldirmak icin.
# "request" paketi ise "api" ye gelen isteklerin icindeki datalari almak icin.
# "jsonify" paketi ise "api" ye gelen isteklere json formatinda data gondermek icin.
from flask import Flask, request, jsonify
from flask_mysqldb import MySQL

load_dotenv(find_dotenv(), override=True)

# Flask uygulamasini instance i olusturulur.
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
mysql = MySQL()
# mysql bilgilerini .env uzantili dosyanini icine yerlestiriyoruz. 'dotenv' ile mysql bilgilerini cekerek
# buradan  gerekli bagalntilari sagliyoruz.
app.config['MYSQL_USER'] = os.environ.get("MYSQL_USER")
app.config['MYSQL_PASSWORD'] = os.environ.get("MYSQL_PASSWORD")
app.config['MYSQL_DB'] = os.environ.get("MYSQL_DB")
app.config['MYSQL_HOST'] = os.environ.get("MYSQL_HOST")
mysql.init_app(app)


# uzak sunucudan json cekmek icin bu izinler gerekli
@app.after_request
def after_request(resp):
    resp.headers.add('Access-Control-Allow-Origin', '*')
    resp.headers.add('Access-Control-Allow-Headers', 'Content-Type, X-Token')
    resp.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
    #resp.headers['Content-Type'] = 'application/json'
    resp.headers['server'] = 'BitirmeServer'
    return resp


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload')
def upload_file():
   return render_template('upload.html')

@app.route('/pics')
def getPictures():
    allofpic = ["uploads/" + pic for pic in os.listdir('uploads')]
    print(allofpic)
    return render_template('pictures.html', pics=allofpic)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
    
@app.route('/uploader', methods = ['POST'])
def uploader_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #return json.dumps({'filename':filename})
            #return redirect(url_for('uploaded_file',
                                  # filename=filename))
            return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


@app.route('/')
def index():
    return jsonify({"status": "okey", "content": "Shut up, bitch!"}), 200

@app.route("/v1/pingpongjson", methods=["POST"])
def pingpongjson():
    data = request.get_json()           # Json datasi istegin icinden alinir.
    return jsonify({data}), 200

@app.route('/v1/temperature/<string:city>', methods=["GET"])
def temperature(city):
    """
    https://home.openweathermap.org
    Activation of an API key for Free and Startup accounts takes 10 minutes. For other accounts it takes from 10 to 60 minutes.
    You can generate as many API keys as needed for your subscription. We accumulate the total load from all of them. 
    """
    r = requests.get("http://api.openweathermap.org/data/2.5/weather?q="+ city +"&appid=" + os.environ.get("OPENWEATHER_KEY"))
    json_object = r.json()
    pprint.pprint(json_object)
    if json_object["cod"] in [200]:
        return jsonify({"status": "okey", "content": json_object }), 200
    else:
        return jsonify({"status": "error", "content": "Api'de sorun var!" }), 400

# "/mysql_test" router'ina istek geldiginde api'nin ayakta oldugu anlamak icin kullandik.
@app.route("/v1/mysql_test")
def hello():
    # Burda mysql istek atiyor, ver donun cevap print ediliyor.
    cur = mysql.connection.cursor()
    cur.execute("select version();")
    # mysql.connection.commit()
    data = cur.fetchall()
    print("tugece")
    return jsonify({"status": "okey", "content": "Ayaktayim, yikilmadim. " + str(data)}), 200


@app.route("/v1/mysql_init")
def init_mysql():
    table_sql = """
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
        "INSERT INTO `user` (username, fullname, password,email) VALUES('ergin123', 'Ergin Cetinhafif' ,'12345','ergin@gmail.com');",
        "INSERT INTO `user` (username, fullname, password,email) VALUES('ceo123'  , 'Ceo Cetin'        ,'12345','ceo@gmail.com');",
    ]
    """

    try:
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO `user` (username, fullname, password,email) VALUES(%s,%s,%s,%s)",
                    ('tugce123', 'Tugce Cetinkaya', '12345', 'tugce@gmail.com'))
        mysql.connection.commit()
    except Exception as e:
        print(e)
        return jsonify({"status": "error", "content": str(e.args[1])}), 500

    return jsonify({"status": "okey", "content": "Tablo yeniden olusturuldu."}), 200

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

# "/v1/create_user" router'ina json datasi ile birlikte istek atilir.(POST)
@app.route("/v1/create_user", methods=["POST"]) #/api/create_user
def create_user():
    data = request.get_json()  # Json datasi istegin icinden alinir.
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
        cur.execute("INSERT INTO `user` (username, fullname, password,email) VALUES(%s,%s,%s,%s)",
                    (newuser['username'], newuser['fullname'], newuser['password'], newuser['email']))
        mysql.connection.commit()
    except Exception as e:
        print(e)
        return jsonify({"status": "error", "content": str(e.args[1])}), 500

    return jsonify({"status": "okey", "content": "Kayit basarili, User olusturdum."}), 200

#Database kayitli user lari gosterir
@app.route("/v1/show_users", methods=["GET"])
def showusers():
    users_info = ""
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM `user`")
        users_info = cur.fetchall() 
    except Exception as e:
        print(e)
    return jsonify({"status": "okey", "data": users_info}),200



# "/api/user/ergin" veya "/api/user/tugce" normal istek atilir(GET). Ve user nin bilgileri istek atilana geri dondurulur.
@app.route("/v1/user/<string:username>", methods=["GET"])
def get_user_information(username):
    print("Okunacak username: ", username)
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

    except Exception as e:
        print(e)  # (1026, 'email or username is not unique')
        return jsonify({"status": "error", "content": str(e.args[1])}), 500  # 'email or username is not unique'

    return jsonify({"status": "okey", "data": user_info}), 200


# "/api/user/ergin" istek atilir ama istegin icinde json olur. Cunku Update islemi gerceklestiriliyor.
@app.route("/v1/user/<string:currentusername>", methods=["PUT"])
def update_user_information(currentusername):
    data = request.get_json()  # Json datasi istegin icinden alinir.
    print(data)
    print("Guncellenecek username: ", currentusername, " Ve degistirilecek data: ", data)
    try:
        cur = mysql.connection.cursor()
        cur.execute(
            "UPDATE `user` SET `username`='{1}', `fullname`='{2}', `password`='{3}', `email`='{4}' WHERE `username`='{0}'".format(
                currentusername, data['username'], data['fullname'], data['password'], data['email']))
        mysql.connection.commit()
    except Exception as e:
        print(e)
        return jsonify({"status": "error", "content": str(e.args[1])}), 500

    return jsonify({"status": "okey", "data": data}), 200


# "/api/user/ergin" istek atilir. Ve dlete islemi gerceklesir.
@app.route("/v1/user/<string:username>", methods=["DELETE"])
def delete_user(username):
    print("Silinecek username: ", username)
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM `user` WHERE `username`='{0}'".format(username))
        mysql.connection.commit()
    except Exception as e:
        print(e)
        return jsonify({"status": "error", "content": str(e.args[1])}), 500

    return jsonify({"status": "okey", "content": "fuck off"}), 200


if __name__ == "__main__":
    app.run()
