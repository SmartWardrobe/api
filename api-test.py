from flask import Flask, render_template
import requests
import json

# Bu kod Ionic gibi davranicak.

app = Flask(__name__)

# Web te form gosterilir. Ve form'dan api'ye istek atilir.
@app.route("/formtest")
def main():
    # templates folder ina bakiyor.
	return render_template("index.html", title="Sign") 

# Api'ye post istegi atiliyor, ionic'ten atiliyormus gibi.
@app.route("/create_user")
def create_user_with_api():
    url = "http://localhost:5000/api/create_user"
    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    data = {
        "username": "tugce",
        "email": "tugce@tugce.com",
        "password": "123456"
    }
    response = requests.post(url, data=json.dumps(data), headers=headers)   # Api'te istegi attigimiz yer.
    responseJson = response.json()
    if responseJson["status"] == "okey":
        print("Status okey geldi.")
        return "200"
    return "400"

# Api'ye get istegi atiliyor, ionic'ten atiliyormus gibi.
@app.route("/user/<string:username>/get")
def get_user_info_from_api(username):
    url = "http://localhost:5000/api/user/" + str(username)
    headers = {'Content-type': 'text/html', 'Accept': 'application/json'}
    r = requests.get(url, headers=headers)
    print(r.json()) # <class 'dict'> tipinde
    return str(r.status_code)

# Api'ye get istegi atiliyor, ionic'ten atiliyormus gibi.
@app.route("/user/<string:username>/put")
def update_user_info_with_api(username):
    url = "http://localhost:5000/api/user/" + str(username)
    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    newdata = {
        "username": "tugce",
        "email": "tugce____asdaksdjasjd@tugce.com",
        "password": "12345678"
    }
    r = requests.put(url, data=json.dumps(newdata), headers=headers)
    rJson = r.json()
    print(rJson)
    if rJson["status"] == "okey":
        print("Status okey geldi.")
        return "200"
    return str(r.status_code)

# Api'ye get istegi atiliyor, ionic'ten atiliyormus gibi.
@app.route("/user/<string:username>/delete")
def delete_user_info_with_api(username):
    url = "http://localhost:5000/api/user/" + str(username)
    headers = {'Content-type': 'text/html', 'Accept': 'application/json'}
    r = requests.delete(url, headers=headers)
    print(r.json()) # <class 'dict'> tipinde
    return str(r.status_code)

if __name__ == "__main__":
    app.run(port=5001)
    