import network
import rp2
import time

network_status = {
    "3" : "Connection established",
    "2" : "No IP",
    "1" : "Joining Network",
    "0" : "Link Down",
    "-1" : "Other Failure",
    "-2" : "Network not found",
    "-3" : "Bad Auth / Invalid Credentials"
}

def wifi_connect(SSID: str, PASSWORD: str, COUNTRY: str, while_connecting: callable):
    rp2.country(COUNTRY)
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    
    max_wait = 10
    
    while max_wait > 0:
        while_connecting(wlan, wlan.status())
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print('waiting for connection: status ' + str(wlan.status()))
        time.sleep(0.1)
        
    # Handle connection error
    if wlan.status() != 3:
        status = str(wlan.status())
        message = 'wifi failed: status [' + status + ']: ' + network_status[status]
        print(message)

    else:
        status = wlan.ifconfig()
        print('connected to [' + SSID + ']')
        print('ip = ' + status[0])

    return wlan