"""
    Flask App uygulamasi
"""
import pprint
import os
import requests
from flask import Flask, request, jsonify, render_template, redirect, send_from_directory
from werkzeug.utils import secure_filename
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(), override=True)

import MysqlOps
import Util
import AwsOps

# Flask uygulamasini instance i olusturulur.
app = Flask(__name__)

UPLOAD_FOLDER = './uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app = MysqlOps.init(app)

# ionic'ten uzak sunucudan json cekmek icin bu izinler gerekli
@app.after_request
def after_request(resp):
    resp.headers.add('Access-Control-Allow-Origin', '*')
    resp.headers.add('Access-Control-Allow-Headers', 'Content-Type, X-Token')
    resp.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
    resp.headers['server'] = 'BitirmeServer'
    return resp

@app.route('/v2/upload_form')
def upload_file_with_form():
    return render_template('upload_form.html')

@app.route('/v2/upload/pic', methods=["POST"])
def upload_pic():
    """
        get file in request.file
        saves in pics directory
        save photo info in mysql
        save photo aws s3 bucket
    """
    username = "anonymus"
    realfilename = ""

    file = request.files.get('file', None)
    if file is None:
        return jsonify({"status": "error", "content": "the post request has the file part"}), 500

    if file.filename == '':
        print("No selected file")
        return jsonify({"status": "error", "content": "No selected file"}), 500

    if file and Util.allowed_file(file.filename):
        realfilename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], realfilename))

        filename, err = MysqlOps.insert_photo(username, realfilename)
        if err:
            return jsonify({"status": "error", "content": str(err.args[1])}), 500

        #AwsOps.upload_pic_to_s3_bucket(file.read(), filename)
        with open("uploads/{}".format(realfilename), "rb") as file:
            AwsOps.upload_pic_to_s3_bucket(file, filename)

        print("Uploaded: {}".format(filename))
        return jsonify({"status": "okey", "filename": filename}), 200

    return jsonify({"status": "error", "content": "Not allowed file"}), 500

@app.route('/v1/pic/<string:photoname>', methods=["GET"])
def get_pic_by_photoname(photoname):
    """
        first check pics directory, if it is exists, return file
        if it is not exists, download pic in aws s3
        then return file
    """
    print(photoname)
    filepath = app.config['UPLOAD_FOLDER'] + '/' + photoname
    if os.path.exists(filepath):
        return send_from_directory(app.config['UPLOAD_FOLDER'], photoname)
    elif MysqlOps.is_photo_exists(photoname):
        AwsOps.download_pic_in_s3_bucket(photoname)
        return send_from_directory(app.config['UPLOAD_FOLDER'], photoname)
    return "I'm sorry"

@app.route('/v1/pic', methods=["PUT"])
def update_pic():
    data = request.get_json()
    print(data)
    filename = data['filename']
    color = data['color']
    typevalue = data['type']
    username = data['username']
    pics, err = MysqlOps.update_photo(username, filename, color, typevalue)
    print(pics)
    print(err)
    if err is None:
        return jsonify({"status": "okey", "pics": pics}), 200

    return jsonify({"status": "error", "content": err}), 500

@app.route('/v1/pic/<string:filename>', methods=["DELETE"])
def delete_pic(filename):
    print(filename)
    result, err = MysqlOps.delete_photo(filename)
    print(result)
    print(err)
    if err is None:
        return jsonify({"status": "okey", "content": "Okey, deleted photo."}), 200

    return jsonify({"status": "error", "content": err}), 500

@app.route('/')
def index():
    return jsonify({"status": "okey", "content": "Shut up, bitch!"}), 200

@app.route("/v1/pingpongjson", methods=["POST"])
def pingpongjson():
    data = request.get_json()           # Json datasi istegin icinden alinir.
    print(data)
    return jsonify({data}), 200

# "/mysql_test" router'ina istek geldiginde api'nin ayakta oldugu anlamak icin kullandik.
@app.route("/v1/mysql_test")
def hello():
    data, err = MysqlOps.get_version()
    print(data)
    print(err)
    if err is None:
        return jsonify({"status": "okey", "content": "Ayaktayim, yikilmadim. " + str(data)}), 200

    return jsonify({"status": "error", "content": str(err.args[1])}), 500

@app.route("/v1/project_init")
def init_project():
    result, err = MysqlOps.create_tables()
    print(result)
    print(err)
    result = AwsOps.clear_files_in_s3_bucket()
    print(result)
    users = [
        {
            "username": "anonymus",
            "fullname": "Anonymus",
            "password": "12345",
            "email": "anonymus@anonymus",
            "photoname": "efuli.png",
            "color": "blue",
            "type": "bottom"
        },
        {
            "username": "tugce123",
            "fullname": "Tugce Cetinkaya",
            "password": "12345",
            "email": "tugce@gmail.com",
            "photoname": "tugce.jpg",
            "color": "red",
            "type": "top"
        }
    ]
    
    for user in users:
        result, err = MysqlOps.insert_user(
            user['username'],
            user['fullname'],
            user['password'],
            user['email']
        )
        print(result)
        print(err)
        if err != None:
            return jsonify({"status": "error", "content": str(err.args[1])}), 500

        filename, err = MysqlOps.insert_photo(user['username'], user['photoname'])
        print(result)
        print(err)
        if err != None:
            return jsonify({"status": "error", "content": str(err.args[1])}), 500

        pics, err = MysqlOps.update_photo(user['username'], filename, user['color'], user['type'])
        print(pics)
        print(err)
        if err != None:
            return jsonify({"status": "error", "content": err }), 500

        with open("uploads/" + user["photoname"], "rb") as file:
            AwsOps.upload_pic_to_s3_bucket(file, filename)

    return jsonify({"status": "okey", "content": "Tablolar olusturuldu.Ve hazir kisi ve photo eklendi."}), 200

@app.route('/v1/show/pics')
def show_pics():
    allofpic = ["/v1/pic/" + pic for pic in os.listdir('uploads')]
    print(allofpic)
    return render_template('pictures.html', pics=allofpic)

@app.route('/v1/show/photonames')
def show_photonames():
    photonames = MysqlOps.get_photonames()
    print(photonames)
    return render_template('photonames.html', photonames=photonames[0])

@app.route('/v1/show/bucketsNfiles')
def show_buckets_N_files():
    bucket_list = AwsOps.get_bucket_list_in_s3()
    file_list = AwsOps.get_file_list_in_s3_bucket()
    print(bucket_list, file_list)
    return render_template('bucketsNfiles.html', buckets=bucket_list, files=file_list)

# "/v1/users" router'ina json datasi ile birlikte istek atilir.(POST)
@app.route("/v1/users", methods=["POST"])
def create_user():
    data = request.get_json()  # Json datasi istegin icinden alinir.
    print(data)
    result, err = MysqlOps.insert_user(
        data['username'],
        data['fullname'],
        data['password'],
        data['email']
    )
    print(result)
    print(err)
    if err is None:
        return jsonify({"status": "okey", "content": "Kayit basarili, User olusturdum."}), 200

    return jsonify({"status": "error", "content": str(err.args[1])}), 500

# "/v1/users" router'ina normal istek atilir. Database kayitli user lari gosterir
@app.route("/v1/users", methods=["GET"])
def get_users():
    users_info, err = MysqlOps.get_users()
    print(users_info)
    print(err)
    if err is None:
        return jsonify({"status": "okey", "data": users_info}), 200

    return jsonify({"status": "error", "content": str(err.args[1])}), 500

# "/v1/user" router'ina normal istek atilir. Database kayitli user'in bilgilerini gonderir.
@app.route("/v1/login", methods=["POST"])
def login():
    # curl -H "Content-Type: application/json" -X POST -d '{"email":"tug@gmail.com","password":"12345"}' http://localhost:5000/v1/login
    data = request.get_json()
    print(data)
    user_info, err = MysqlOps.login(data["email"], data["password"])
    print(user_info)
    print(err)
    if err is None:
        return jsonify({"status": "okey", "data": user_info}), 200

    return jsonify({"status": "error", "content": str(err)}), 500

# "/api/user/ergin" veya "/api/user/tugce" normal istek atilir(GET). Ve user nin bilgileri istek atilana geri dondurulur.
@app.route("/v1/user/<string:username>", methods=["GET"])
def get_user_information(username):
    print("Okunacak username: ", username)
    result, err = MysqlOps.get_user_information_by_username(username)
    print(result)
    print(err)
    if err is None:
        return jsonify({"status": "okey", "data": result}), 200

    return jsonify({"status": "error", "content": str(err)}), 500  # 'email or username is not unique'

@app.route('/v1/user/<string:username>/pics', methods=["GET"])
def get_user_pics_list(username):
    """
        read mysql, then learn filenames
        return filename list
    """
    print(username)
    pics, err = MysqlOps.get_user_pics_by_username(username)
    print(pics)
    if err is None:
        return jsonify({"status": "okey", "data": pics}), 200

    return jsonify({"status": "error", "content": str(err.args[1])}), 500

# "/api/user/ergin" istek atilir ama istegin icinde json olur. Cunku Update islemi gerceklestiriliyor.
@app.route("/v1/user/<string:currentusername>", methods=["PUT"])
def update_user_information(currentusername):
    data = request.get_json()  # Json datasi istegin icinden alinir.
    print(data)
    print("Guncellenecek username: ", currentusername, " Ve degistirilecek data: ", data)
    result, err = MysqlOps.update_user_information_by_username(currentusername, data)
    print(result)
    print(err)
    if err is None:
        return jsonify({"status": "okey", "data": data}), 200
    return jsonify({"status": "error", "content": str(err.args[1])}), 500

# "/api/user/ergin" istek atilir. Ve dlete islemi gerceklesir.
@app.route("/v1/user/<string:username>", methods=["DELETE"])
def delete_user(username):
    print("Silinecek username: ", username)
    result, err = MysqlOps.delete_user_by_username(username)
    print(result)
    print(err)
    if err is None:
        return jsonify({"status": "okey", "content": "fuck off"}), 200

    return jsonify({"status": "error", "content": str(err.args[1])}), 500

@app.route('/v1/temperature/<string:city>', methods=["GET"])
def temperature(city):
    """
    https://home.openweathermap.org
    Activation of an API key for Free and Startup accounts takes 10 minutes.
    For other accounts it takes from 10 to 60 minutes.
    You can generate as many API keys as needed for your subscription.
    We accumulate the total load from all of them.
    """
    r = requests.get("http://api.openweathermap.org/data/2.5/weather?q="+ city +"&appid=" + os.environ.get("OPENWEATHER_KEY"))
    json_object = r.json()
    pprint.pprint(json_object)
    if json_object["cod"] in [200]:
        return jsonify({"status": "okey", "content": json_object}), 200
    else:
        return jsonify({"status": "error", "content": "Api'de sorun var!"}), 400

if __name__ == "__main__":
    app.run()
