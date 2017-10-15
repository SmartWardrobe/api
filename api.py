# "Flask" paketini kullanmamizin sebebi uygulamayi ayaga kaldirmak icin.
# "request" paketi ise "api" ye gelen isteklerin icindeki datalari almak icin.
# "jsonify" paketi ise "api" ye gelen isteklere json formatinda data gondermek icin.
from flask import Flask, request, jsonify

# Flask uygulamasini instance i olusturulur.
app=Flask(__name__)


# "/" router'ina istek geldiginde api'nin ayakta oldugu anlamak icin kullandik.
@app.route("/")
def hello():
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
# Suanlik ayri flask uygulamasindan "requests" paketiyle post,put,get,delete istegi aticaz. Ionic'le test etmek biraz daha ugrastirici suanlik.
# Ve ilerde mysql'de deneme yaparsiniz. Suanlik static kullanim yapin.
# Bir ileri adimda Authorization

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
    return jsonify({"status": "okey"})

# "/api/user/ergin" veya "/api/user/tugce" normal istek atilir(GET). Ve user nin bilgileri istek atilana geri dondurulur.
@app.route("/api/user/<string:username>", methods=["GET"])
def get_user_information(username):
    # Read islemi
    print("Okunacak username: ", username)
    return jsonify({"status": "okey", "data": "..."})

# "/api/user/ergin" istek atilir ama istegin icinde json olur. Cunku Update islemi gerceklestiriliyor.
@app.route("/api/user/<string:username>", methods=["PUT"])
def update_user_information(username):
    data = request.get_json()
    print(data)
    # Update islemi
    print("Guncellenecek username: ", username, " Ve degistirilecek data: ", data)
    return jsonify({"status": "okey", "data": "..."})

# "/api/user/ergin" istek atilir. Ve dlete islemi gerceklesir.
@app.route("/api/user/<string:username>", methods=["DELETE"])
def delete_user(username):
    # delete islemi
    print("Silinecek username: ", username)
    return jsonify({"status": "okey"})

if __name__ == "__main__":
    app.run(port=5000)
