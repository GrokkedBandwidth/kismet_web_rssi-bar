import requests

class Mac:
    def __init__(self):
        self.username = 'kismet'
        self.password = 'kismet'
        self.IP = '192.168.1.167'
        self.mac = "FF:FF:FF:FF:FF:FF"
        self.best_seen = -120
        self.last_seen_time = 0
        self.last_best_time = 0
        self.current_channel = 0
        self.url = f"http://{self.username}:{self.password}@{self.IP}:2501/"
        self.source_params = {
            'fields': [
                'kismet.datasource.channels',
                'kismet.datasource.uuid',
                "kismet.datasource.interface",
                "kismet.datasource.hopping",
                "kismet.datasource.channel",
                "kismet.datasource.hop_channels"
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
        self.one_six_eleven_params = {
            'channels': ['1', '6', '11'],
            'hoprate': 5
        }
        self.two_full_params = {
            'channels': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14'],
            'hoprate': 5
        }
        self.five_full_params = {
            'channels': ['36', '40', '44', '48', '52', '56', '60', '64', '100', '104', '108', '112', '116', '120',
                         '124',
                         '128', '132', '136', '140', '144', '149', '153', '157', '161', '165'],
            'hoprate': 5
        }
        self.interfaces = []

    def retrieve_mac(self):
        results = requests.post(
            url=f"{self.url}devices/by-mac/{self.mac}/devices.json",
            json=self.target_params
        ).json()
        return results

    def get_interfaces(self):
        results = requests.post(
            url=f"{self.url}datasource/all_sources.json",
            json=self.source_params).json()
        self.interfaces = results

    def survey_channels(self, uuid, span):
        if span == "all":
            for item in self.interfaces:
                if item['kismet.datasource.uuid'] == uuid:
                    params = {
                        'channels': item['kismet.datasource.channels'],
                        'hoprate': 5
                    }

                    requests.post(
                        url=f"{self.url}datasource/by-uuid/{uuid}/set_channel.cmd",
                        json=params)
        else:
            requests.post(
                url=f"{self.url}datasource/by-uuid/{uuid}/set_channel.cmd",
                json=span)

    def lock_channel(self, uuid, channel):
        requests.post(
            url=f"{self.url}datasource/by-uuid/{uuid}/set_channel.cmd",
            json={'channel': channel})




