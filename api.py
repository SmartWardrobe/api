# "Flask" paketini kullanmamizin sebebi uygulamayi ayaga kaldirmak icin.
# "request" paketi ise "api" ye gelen isteklerin icindeki datalari almak icin.
# "jsonify" paketi ise "api" ye gelen isteklere json formatinda data gondermek icin.
from flask import Flask, request, jsonify

# Database Class ile veri tabani ayarlari ayarlaniyor.
# query() metodu ise SQL komutlarini calistirip, sonuclari aliyor.
# query() icinde connection cursor islemleri gerceklesiyor, otamatik kapatiliyor.
# Daha fazla bilgi icin kod burda: https://github.com/pleycpl/my_flask_mysql_connector 
# Ya da flask_mysql paketi daha avantajli olabilir. Arastirmak lazim.
from my_flask_mysql_connector.MysqlDb import Database
mysql = Database("localhost", 3306, "root", "", "testdb")

# Flask uygulamasini instance i olusturulur.
app=Flask(__name__)


# "/" router'ina istek geldiginde api'nin ayakta oldugu anlamak icin kullandik.
@app.route("/")
def hello():
    # Burda mysql istek atiyor, ver donun cevap print ediliyor.
    results = mysql.query("Select version();")
    print(results)
    return "Ayaktayim, yikilmadim."

# "/api/signwebform" router'ina web form dan "action" kismindan gelen istekleri karsilamak icin kullandik.
@app.route("/api/signwebform", methods=["POST"])
def sign():
    username= str(request.form["username"])
    password=str(request.form["password"])
    email=str(request.form["email"])
    print(username + password + email)
    return username + password + email


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
    return jsonify({"status": "okey", "content": "User olusturdum."})

# "/api/user/ergin" veya "/api/user/tugce" normal istek atilir(GET). Ve user nin bilgileri istek atilana geri dondurulur.
@app.route("/api/user/<string:username>", methods=["GET"])
def get_user_information(username):
    print("Okunacak username: ", username)
    # Burda username ile mysql den data aliriz, ve istek atana json formatin da gondeririz.
    return jsonify({"status": "okey", "data": "..."})

# "/api/user/ergin" istek atilir ama istegin icinde json olur. Cunku Update islemi gerceklestiriliyor.
@app.route("/api/user/<string:username>", methods=["PUT"])
def update_user_information(username):
    data = request.get_json()           # Json datasi istegin icinden alinir.
    print(data)
    print("Guncellenecek username: ", username, " Ve degistirilecek data: ", data)
    # Mysql islemleri
    return jsonify({"status": "okey", "data": "..."})

# "/api/user/ergin" istek atilir. Ve dlete islemi gerceklesir.
@app.route("/api/user/<string:username>", methods=["DELETE"])
def delete_user(username):
    print("Silinecek username: ", username)
    # Mysql islemleri
    return jsonify({"status": "okey"})

if __name__ == "__main__":
    app.run(port=5000)