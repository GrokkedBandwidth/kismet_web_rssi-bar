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
    mac.get_interfaces()
    return render_template('index.html', mac=mac.mac, channels=mac.interfaces)

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

@app.route('/<string:uuid>/<string:channel>', methods=['GET'])
def lock_channel(uuid, channel):
    uuid = json.loads(uuid)['uuid']
    channel = json.loads(channel)['channel']
    mac.lock_channel(uuid, channel)
    return f"New channel set for {uuid}"

@app.route('/hop/<string:uuid>/<string:option>', methods=['GET'])
def survey_channels(uuid, option):
    uuid = json.loads(uuid)['uuid']
    option = json.loads(option)['option']
    match option:
        case "one":
            mac.survey_channels(uuid=uuid, span=mac.one_six_eleven_params)
        case "two":
            mac.survey_channels(uuid=uuid, span=mac.two_full_params)
        case "three":
            mac.survey_channels(uuid=uuid, span=mac.five_full_params)
        case "four":
            mac.survey_channels(uuid=uuid, span="all")
        case _:
            pass
    return f"New channels set for {uuid}"

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