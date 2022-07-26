import rp2
import time
import network
from network import WLAN

network_status = {
    "3": "Connection established",
    "2": "No IP",
    "1": "Joining Network",
    "0": "Link Down",
    "-1": "Other Failure",
    "-2": "Network not found",
    "-3": "Bad Auth / Invalid Credentials"
}


class Wifi:
    ssid: str
    password: str
    country: str

    def __init__(self, ssid: str, password: str, country: str):
        self.ssid = ssid
        self.password = password
        self.country = country
        self.wlan = None

    def connect(self, while_connecting: callable):

        if self.wlan and self.wlan.status() == 3:
            print('connection already established')
            return

        rp2.country(self.country)
        self.wlan = WLAN(network.STA_IF)
        self.wlan.active(True)
        self.wlan.connect(self.ssid, self.password)

        max_wait = 10

        while max_wait > 0:
            while_connecting(self)
            if self.status() < 0 or self.status() >= 3:
                break
            max_wait -= 1
            print('waiting for connection: status ' + str(self.status()))
            time.sleep(1)

        # Handle connection error
        if self.status() != 3:
            status = str(self.status())
            print('wifi failed: status [' + status + ']: ' + network_status[status])

        else:
            status = self.wlan.ifconfig()
            print('connected to [' + self.ssid + ']')
            print('ip = ' + status[0])

    def status(self) -> int:
        if self.wlan:
            return self.wlan.status()

        return 0

    def status_str(self):
        return network_status[str(self.status())]

    def ip(self) -> str:
        if self.wlan:
            ifconfig = self.wlan.ifconfig()
            return ifconfig[0]

        return '0.0.0.0'
