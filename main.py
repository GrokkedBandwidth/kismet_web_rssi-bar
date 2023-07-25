from flask import Flask, render_template, Response, redirect, url_for, request
from flask_bootstrap import Bootstrap
import json
import time
from mac import Mac
from random import randint

mac = Mac()

app = Flask(__name__)
Bootstrap(app)

@app.route('/', methods=['POST', 'GET'])
def home():
    return render_template('index.html', mac=mac.mac)

@app.route('/mac', methods=['GET', 'POST'])
def set_mac():
    mac.mac = request.form['mac']
    mac.best_seen = -120
    mac.last_seen = 0
    return redirect(url_for('home', mac=mac))


@app.route('/df', methods=['POST', 'GET'])
def df():
    def generate():
        while True:
            response = {}
            results = mac.retrieve_mac()
            rssi = results[0]['kismet.common.signal.last_signal']
            mac.current_channel = results[0]['kismet.device.base.channel']
            response[0] = 120 - (int(rssi) * -1)
            response[1] = rssi
            response[2] = mac.current_channel
            if rssi > mac.best_seen:
                mac.best_seen = rssi
                mac.last_seen = time.time()
            response[3] = mac.best_seen
            time_since = int(time.time() - mac.last_seen)
            response[4] = time_since
            return_string = 'data:' + json.dumps(response) + "\n\n"
            yield return_string
            time.sleep(.2)
    return Response(generate(), mimetype='text/event-stream')

# @app.route('/lock_channel', methods=['GET'])
# def lock_channel():
#     interface_list = []
#     results = requests.post(
#         url=f"http://{USERNAME}:{PASSWORD}@{IP}:2501/datasource/all_sources.json",
#         json=source_params).json()
#     for item in results:
#         interface_list.append(item['kismet.datasource.uuid'])
#     for item in interface_list:
#         requests.post(
#             url=f"http://{USERNAME}:{PASSWORD}@{IP}:2501/datasource/by-uuid/{item}/set_channel.cmd",
#             json={'channel': current_channel})
#     return f"Channel locked to {current_channel}"

# @app.route('/one_six_eleven', methods=['GET'])
# def one_six_eleven():
#     hop_params = {
#         'channels': ['1', '6', '11'],
#         'hoprate': 5
#     }
#     interface_list = []
#     results = requests.post(
#         url=f"http://{USERNAME}:{PASSWORD}@{IP}:2501/datasource/all_sources.json",
#         json=source_params).json()
#     for item in results:
#         interface_list.append(item['kismet.datasource.uuid'])
#     for item in interface_list:
#         lock = requests.post(
#             url=f"http://{USERNAME}:{PASSWORD}@{IP}:2501/datasource/by-uuid/{item}/set_channel.cmd",
#             json=hop_params, )
#     return f"Hopping 1,6,11"
#
# @app.route('/two_GHz', methods=['GET'])
# def two_GHz():
#     hop_params = {
#         'channels': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14'],
#         'hoprate': 5
#     }
#     interface_list = []
#     results = requests.post(
#         url=f"http://{USERNAME}:{PASSWORD}@{IP}:2501/datasource/all_sources.json",
#         json=source_params).json()
#     for item in results:
#         interface_list.append(item['kismet.datasource.uuid'])
#     for item in interface_list:
#         lock = requests.post(
#             url=f"http://{USERNAME}:{PASSWORD}@{IP}:2501/datasource/by-uuid/{item}/set_channel.cmd",
#             json=hop_params, )
#     return f"Hopping 2GHz"
#
# @app.route('/five_GHz', methods=['GET'])
# def five_GHz():
#     hop_params = {
#         'channels': ['36', '40', '44', '48', '52', '56', '60', '64', '100', '104', '108', '112', '116', '120', '124',
#                      '128', '132', '136', '140', '144', '149', '153', '157', '161', '165'],
#         'hoprate': 5
#     }
#     interface_list = []
#     results = requests.post(
#         url=f"http://{USERNAME}:{PASSWORD}@{IP}:2501/datasource/all_sources.json",
#         json=source_params).json()
#     for item in results:
#         interface_list.append(item['kismet.datasource.uuid'])
#     for item in interface_list:
#         lock = requests.post(
#             url=f"http://{USERNAME}:{PASSWORD}@{IP}:2501/datasource/by-uuid/{item}/set_channel.cmd",
#             json=hop_params, )
#     return f"Hopping 5GHz"
#
# @app.route('/hop_all', methods=['GET'])
# def hop_all():
#     hop_params = {
#         'channels': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14',
#                      '36', '40', '44', '48', '52', '56', '60', '64', '100', '104', '108', '112',
#                      '116', '120', '124', '128', '132', '136', '140', '144', '149', '153', '157', '161', '165'],
#         'hoprate': 5
#     }
#     interface_list = []
#     results = requests.post(
#         url=f"http://{USERNAME}:{PASSWORD}@{IP}:2501/datasource/all_sources.json",
#         json=source_params).json()
#     for item in results:
#         interface_list.append(item['kismet.datasource.uuid'])
#     for item in interface_list:
#         lock = requests.post(
#             url=f"http://{USERNAME}:{PASSWORD}@{IP}:2501/datasource/by-uuid/{item}/set_channel.cmd",
#             json=hop_params, )
#     return f"Hopping all possible channels"

@app.route('/test', methods=['POST', 'GET'])
def test():
    def generate():
        while True:
            response = {}
            randum_num = randint(1, 100)
            response[0] = randum_num
            return_string = 'data:' + json.dumps(response) + "\n\n"
            print(f'{return_string} test data')
            yield return_string
            time.sleep(.2)
    return Response(generate(), mimetype='text/event-stream')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)