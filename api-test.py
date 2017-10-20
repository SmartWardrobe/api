from flask import Flask
import requests
import json

# Bu kod Ionic gibi davranicak.

app = Flask(__name__)


# Api'ye post istegi atiliyor, ionic'ten atiliyormus gibi.
@app.route("/create_user")
def create_user_with_api():
    url = "http://localhost:5000/api/create_user"
    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    data = {
        "username": "tugce",
        "fullname": "Tugce Cetınkaya",
        "email": "tugce@tugce.com",
        "password": "123456"
    }
    response = requests.post(url, data=json.dumps(data), headers=headers)   # Api'te istegi attigimiz yer.
    responseJson = response.json()
    if responseJson["status"] == "okey":
        print("Status okey geldi.")
        return "200"
    elif responseJson["status"] == "error":
        print("Status error geldi.")
        return "400"

    return "500"

# Api'ye get istegi atiliyor, ionic'ten atiliyormus gibi.
@app.route("/user/<string:username>/get")
def get_user_info_from_api(username):
    url = "http://localhost:5000/api/user/" + str(username)
    headers = {'Content-type': 'text/html', 'Accept': 'application/json'}
    r = requests.get(url, headers=headers)
    rJson = r.json()
    print(rJson)                        # <class 'dict'> tipinde
    if rJson['status'] == 'okey':
        return str(rJson['data'])
    elif rJson['status'] == 'error':
        return "404"

    return "default"

# Api'ye get istegi atiliyor, ionic'ten atiliyormus gibi.
@app.route("/user/<string:username>/put")
def update_user_info_with_api(username):
    url = "http://localhost:5000/api/user/" + str(username)
    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    newdata = {
        "username": "tugce789",
        "fullname": "Tugce Cetınkaya",
        "email": "yenitugce@tugce.com",
        "password": "123qweadf"
    }
    r = requests.put(url, data=json.dumps(newdata), headers=headers)
    rJson = r.json()
    print(rJson)                        # <class 'dict'> tipinde
    if rJson['status'] == 'okey':
        return str(rJson['data'])
    elif rJson['status'] == 'error':
        return "404"

    return "default"

# Api'ye get istegi atiliyor, ionic'ten atiliyormus gibi.
@app.route("/user/<string:username>/delete")
def delete_user_info_with_api(username):
    url = "http://localhost:5000/api/user/" + str(username)
    headers = {'Content-type': 'text/html', 'Accept': 'application/json'}
    r = requests.delete(url, headers=headers)
    rJson = r.json()
    print(rJson)                        # <class 'dict'> tipinde
    if rJson['status'] == 'okey':
        return str(rJson['content'])
    elif rJson['status'] == 'error':
        return "404"

    return "default"

if __name__ == "__main__":
    app.run(port=5001)
    