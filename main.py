from flask import Flask, render_template, Response, redirect, url_for, request, jsonify
from flask_bootstrap import Bootstrap
import json
import requests
import time
from random import randint

USERNAME = 'kismet'
PASSWORD = 'kismet'
IP = 'localhost'

app = Flask(__name__)
Bootstrap(app)

source_params = {
    'fields': [
        'kismet.datasource.channels',
        'kismet.datasource.uuid'
    ]
}

target_params = {
    'fields': [
        'kismet.device.base.macaddr',
        "kismet.device.base.last_time",
        "kismet.device.base.signal/kismet.common.signal.last_signal",
        "kismet.device.base.channel",
        'kismet.device.base.location/kismet.common.location.last/kismet.common.location.geopoint',
        'kismet.device.base.key',
        'kismet.common.seenby.uuid'
    ],
    'datatable': True
}

mac = ''
best_seen = -120
last_seen = 0
current_channel = 0

@app.route('/', methods=['POST', 'GET'])
def home():
    global mac
    return render_template('index.html', mac=mac)

@app.route('/mac', methods=['GET', 'POST'])
def set_mac():
    global mac, best_seen, last_seen
    mac = request.form['mac']
    best_seen = -120
    last_seen = 0
    return redirect(url_for('home', mac=mac))


@app.route('/df', methods=['POST', 'GET'])
def df():
    def generate():
        global mac, best_seen, last_seen, current_channel
        while True:
            response = {}
            results = requests.post(
                url=f"http://{USERNAME}:{PASSWORD}@{IP}:2501/devices/by-mac/{mac}/devices.json",
                json=target_params
            ).json()
            rssi = results[0]['kismet.common.signal.last_signal']
            current_channel = results[0]['kismet.device.base.channel']
            response[0] = 120 - (int(rssi) * -1)
            response[1] = rssi
            response[2] = current_channel
            if rssi > best_seen:
                best_seen = rssi
                last_seen = time.time()
            response[3] = best_seen
            time_since = int(time.time() - last_seen)
            response[4] = time_since
            return_string = 'data:' + json.dumps(response) + "\n\n"
            yield return_string
            time.sleep(.2)
    return Response(generate(), mimetype='text/event-stream')

@app.route('/lock_channel', methods=['GET'])
def lock_channel():
    interface_list = []
    results = requests.post(
        url=f"http://{USERNAME}:{PASSWORD}@{IP}:2501/datasource/all_sources.json",
        json=source_params).json()
    for item in results:
        interface_list.append(item['kismet.datasource.uuid'])
    for item in interface_list:
        requests.post(
            url=f"http://{USERNAME}:{PASSWORD}@{IP}:2501/datasource/by-uuid/{item}/set_channel.cmd",
            json={'channel': current_channel})
    return results

@app.route('/test', methods=['POST', 'GET'])
def test():
    def generate():
        while True:
            response = {}
            randum_num = randint(1,100)
            response[0] = randum_num
            return_string = 'data:' + json.dumps(response) + "\n\n"
            print(f'{return_string} test data')
            yield return_string
            time.sleep(.2)
    return Response(generate(), mimetype='text/event-stream')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)