import requests

class Mac:
    def __init__(self):
        self.username = 'kismet'
        self.password = 'kismet'
        self.IP = '192.168.1.167'
        self.mac = "FF:FF:FF:FF:FF:FF"
        self.best_seen = -120
        self.last_seen = 0
        self.current_channel = 0
        self.url = f"http://{self.username}:{self.password}@{self.IP}:2501/"
        self.source_params = {
            'fields': [
                'kismet.datasource.channels',
                'kismet.datasource.uuid'
            ]
        }
        self.target_params = {
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
    def retrieve_mac(self):
        results = requests.post(
            url=f"{self.url}devices/by-mac/{self.mac}/devices.json",
            json=self.target_params
        ).json()
        return results




