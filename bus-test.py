import config
from src.event_bus.bus import EventBus
from src.RTCFactory import RTCFactory
from src.Request import Request
from src.control.Buttons import Buttons
from src.ical.ApiParser import ApiParser
from src.ical.EventManager import EventManager
from src.model.Date import Date
from src.view.Display import Display
from src.wifi import wifi_connect

# registering some important global variables
wifi = None
event_manager = None # 'EventManager'
bus = EventBus()
display = Display()
buttons = Buttons()

@bus.on('wifi.connect')
def subscribed_event():
    def while_connecting(wlan, status):
        display.render_connecting(wlan, status)

    global wifi
    wifi = wifi_connect(
        config.WIFI_SSID,
        config.WIFI_PASSWORD,
        config.WIFI_COUNTRY,
        while_connecting
    )

    bus.emit('wifi.status', wifi)
    if wifi.status() == 3:
        now = RTCFactory.init_rtc()
        bus.emit('data.load')


@bus.on('wifi.status')
def subscribed_event2(wifi):
    display.render_wifi_status(wifi)


@bus.on('data.load')
def data_load():
    json = Request.get_json(config.ICAL_URL)
    Api = ApiParser(json)
    events = Api.parse_response()

    global event_manager
    if event_manager is None:
        event_manager = EventManager(
            Date.from_rtc(RTCFactory.rtc),
            RTCFactory.rtc,
            events
        )

    display.render_events_loaded(event_manager)


@bus.on('button.pressed')
def render_time():
    display.render_current_time(event_manager)


if __name__ == '__main__':
    print('')
    bus.emit('wifi.connect')

    while True:

        event_manager.update_from_rtc()

        if Buttons.any_pressed():
            bus.emit('button.pressed')
        else:
            display.render_idle()