from flask import Flask, render_template, request
import requestsz

app = Flask(__name__)

@app.route('/temperature', methods=['POST'])
def temperature():
    zipcode = request.form['zip']
    r = requests.get('http://api.openweathermap.org/data/2.5/weather?zip='+zipcode+',745044&appid=e4ab38d89e4cf6f2db75187d50509bcd')
    json_object = r.json()
    print(json_object)
    temp_k = float(json_object['main']['temp'])
    temp_f = (temp_k - 273.15) * 1.8 + 32
    return render_template('temperature.html', temp=temp_f)
    
@app.route('/')
def index():
	return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

print(zipcode, r, json_object, temp_k, temp_f)