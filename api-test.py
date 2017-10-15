from flask import Flask, render_template
import requests
import json

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
        "username": "ergin",
        "email": "ergin@ergin.com",
        "password": "123456"
    }
    r = requests.post(url, data=json.dumps(data), headers=headers)
    print(r)
    print(r.json())
    return r.status_code

# Api'ye get istegi atiliyor, ionic'ten atiliyormus gibi.
@app.route("/user/<string:username>")
def get_user_info_from_api(username):
    url = "http://localhost:5000/api/user/" + str(username)
    headers = {'Content-type': 'text/html', 'Accept': 'application/json'}
    r = requests.get(url, headers=headers)
    print(r.json()) # <class 'dict'> tipinde
    return r.status_code

if __name__ == "__main__":
    app.run(port=5001)
    