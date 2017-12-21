import os, json, pprint
import requests
from flask import Flask, request, jsonify, render_template, redirect, url_for, send_from_directory, flash
from werkzeug.utils import secure_filename
from flask import Flask, request, jsonify
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
    #resp.headers['Content-Type'] = 'application/json'
    resp.headers['server'] = 'BitirmeServer'
    return resp


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
    print("ILk kisim: ", request.method)
    if request.method == 'POST':
        # check if the post request has the file part
        print(request.files)
        if 'file' not in request.files:
            #flash('No file part')
            print("No file part")
            return "Haaaaaa"#redirect(request.url)

        print("3.cu kisim")
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        print("4.cu kisim")
        if file.filename == '':
            #flash('No selected file')
            return redirect(request.url)
        if file and Util.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #return json.dumps({'filename':filename})
            #return redirect(url_for('uploaded_file',
                                  # filename=filename))
            return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/v1/upload_pic', methods=["POST"])
def upload_pic():
    # get file in request.file
    # saves in pics directory
    # save photo info in mysql
    # save photo aws s3 bucket
    """
    with open("pics/efuli.png", "rb") as file:
        AwsOps.upload_pic_to_s3_bucket(file, 'efuli.png')

    return jsonify({"status": "okey", "content": "okey i uploaded"}), 200
    """
    return ""

@app.route('/v1/get_user_pics_list', methods=["GET"])
def get_user_pics_list():
    # read mysql, then learn photoids
    # return photoid list
    return ""

@app.route('/v1/get_pic/<string:photoid>', methods=["GET"])
def get_pic_by_photoid(photoid):
    # first check pics directory, if it is exists, return file
    # if it is not exists, download pic in aws s3
    # AwsOps.download_pic_in_s3_bucket(username + "_" + filename)
    # then return file
    return ""

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
    data, err = MysqlOps.get_version()
    print(data)
    print(err)
    if err == None:
        return jsonify({"status": "okey", "content": "Ayaktayim, yikilmadim. " + str(data)}), 200

    return jsonify({"status": "error", "content": str(err.args[1])}), 500

@app.route("/v1/project_init")
def init_mysql():
    result, err = MysqlOps.create_tables()
    print(result)
    print(err)
    result, err = MysqlOps.insert_user('tugce123', 'Tugce Cetinkaya', '12345', 'tugce@gmail.com')
    print(result)
    print(err)
    if err != None:
        return jsonify({"status": "error", "content": str(err.args[1])}), 500

    date = MysqlOps.get_time()
    result, err = MysqlOps.insert_photo('tugce123', date)
    print(result)
    print(err)
    if err != None:
        return jsonify({"status": "error", "content": str(err.args[1])}), 500

    with open("pics/efuli.png", "rb") as file:
        AwsOps.upload_pic_to_s3_bucket(file, 'tugce123_' + date + '.png')

    return jsonify({"status": "okey", "content": "Tablolar olusturuldu.Ve hazir kisi ve photo eklendi."}), 200


# "/v1/create_user" router'ina json datasi ile birlikte istek atilir.(POST)
@app.route("/v1/create_user", methods=["POST"]) #/api/create_user
def create_user():
    data = request.get_json()  # Json datasi istegin icinden alinir.
    print(data)
    result, err = MysqlOps.insert_user(data['username'], data['fullname'], data['password'], data['email'])
    print(result)
    print(err)
    if err == None:
        return jsonify({"status": "okey", "content": "Kayit basarili, User olusturdum."}), 200
    
    return jsonify({"status": "error", "content": str(err.args[1])}), 500

#Database kayitli user lari gosterir
@app.route("/v1/show_users", methods=["GET"])
def showusers():
    users_info, err = MysqlOps.get_users()
    print(users_info)
    print(err)
    if err == None:
        return jsonify({"status": "okey", "data": users_info}),200

    return jsonify({"status": "error", "content": str(err.args[1])}), 500

# "/api/user/ergin" veya "/api/user/tugce" normal istek atilir(GET). Ve user nin bilgileri istek atilana geri dondurulur.
@app.route("/v1/user/<string:username>", methods=["GET"])
def get_user_information(username):
    print("Okunacak username: ", username)
    result, err = MysqlOps.get_user_information_by_username(username)
    print(result)
    print(err)
    if err == None:
        return jsonify({"status": "okey", "data": result}), 200

    return jsonify({"status": "error", "content": str(err.args[1])}), 500  # 'email or username is not unique'


# "/api/user/ergin" istek atilir ama istegin icinde json olur. Cunku Update islemi gerceklestiriliyor.
@app.route("/v1/user/<string:currentusername>", methods=["PUT"])
def update_user_information(currentusername):
    data = request.get_json()  # Json datasi istegin icinden alinir.
    print(data)
    print("Guncellenecek username: ", currentusername, " Ve degistirilecek data: ", data)
    result, err = MysqlOps.update_user_information_by_username(currentusername, data)
    print(result)
    print(err)
    if err == None:
        return jsonify({"status": "okey", "data": data}), 200
    return jsonify({"status": "error", "content": str(err.args[1])}), 500

# "/api/user/ergin" istek atilir. Ve dlete islemi gerceklesir.
@app.route("/v1/user/<string:username>", methods=["DELETE"])
def delete_user(username):
    print("Silinecek username: ", username)
    result, err = MysqlOps.delete_user_by_username(username)
    print(result)
    print(err)
    if err == None:
        return jsonify({"status": "okey", "content": "fuck off"}), 200

    return jsonify({"status": "error", "content": str(err.args[1])}), 500

if __name__ == "__main__":
    app.run()
