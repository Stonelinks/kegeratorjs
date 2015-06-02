from flask import Flask, jsonify
import random

# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_folder='../../build')

fake_flowmeter_counter1 = 0
fake_flowmeter_counter2 = 0

@app.route('/')
def root():
    return app.send_static_file('index.html')

# hilariously insecure
@app.route('/<path:path>')
def send_static(path):
    return app.send_static_file(path)

@app.route('/sensor_data')
def send_sensor_data():
    global fake_flowmeter_counter1, fake_flowmeter_counter2
    sensor_data = {
      "thermostat": random.random() * 100.0,
      "flowmeters": [fake_flowmeter_counter1, fake_flowmeter_counter2]
    }
    fake_flowmeter_counter1 += 1
    fake_flowmeter_counter2 += 2
    return jsonify(**sensor_data)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
