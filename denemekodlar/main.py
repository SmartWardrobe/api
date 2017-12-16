from flask import Flask, render_template, request
import requests, os

app = Flask(__name__)

@app.route('/temperature/<string:city>')
def temperature(city):

    OPENWEATHER_KEY = "e4ab38d89e4cf6f2db75187d50509bcd"
    city = "London"
    r = requests.get("http://samples.openweathermap.org/data/2.5/weather?q="+ city + os.environ.get("OPENWEATHER_KEY"))
    json_object = r.json()

    print(json_object)

    return jsonify({"status": "okey", "content": "Aferin" }), 200
