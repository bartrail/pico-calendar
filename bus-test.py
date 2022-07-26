from time import sleep
import gc

import config
from src.event_bus.bus import EventBus
from src.RTCFactory import RTCFactory
from src.Request import Request
from src.control.Buttons import Buttons
from src.ical.ApiParser import ApiParser
from src.ical.EventManager import EventManager
from src.model.Date import Date
from src.view.Display import Display
from src.wifi import Wifi

# registering some important global variables
wifi = Wifi(config.WIFI_SSID, config.WIFI_PASSWORD, config.WIFI_COUNTRY)
event_manager = None # 'EventManager'
bus = EventBus()
display = Display()
buttons = Buttons()

@bus.on('wifi.connect')
def wifi_connect():
    def while_connecting(wlan: 'Wifi'):
        display.render_connecting(wlan)

    wifi.connect(while_connecting)

    bus.emit('wifi.status', wifi)
    if wifi.status() == 3:
        now = RTCFactory.init_rtc()
        bus.emit('data.load')


@bus.on('wifi.status')
def wifi_status(wifi):
    display.render_wifi_status(wifi)


@bus.on('data.load')
@bus.on('button.pressed.down')
def data_load():
    display.render_loading_data()
    try:
        if Request.is_loading:
            return

        json = Request.get_json(config.ICAL_URL)
        Api = ApiParser(json)
        events = Api.parse_response()
        del json

        global event_manager
        if event_manager is None:
            event_manager = EventManager(
                Date.from_rtc(RTCFactory.rtc),
                RTCFactory.rtc,
                events
            )
        else:
            event_manager.update_events(events)

        display.render_events_loaded(event_manager)

    except BaseException as error:
        display.render_error('Error loading Data!', error)
        raise error


@bus.on('button.pressed.a')
def render_time():
    display.render_current_time(event_manager)


@bus.on('button.pressed.b')
def render_time():
    display.render_events_loaded(event_manager)


@bus.on('button.pressed.a.b.center')
def exit():
    display.render_error('Exit.', None)
    raise SystemExit('exit')

if __name__ == '__main__':
    bus.emit('wifi.connect')

    if event_manager is None:
        print('EventManager is not initialized')
        raise SystemExit('exit')

    while True:

        event_manager.update_from_rtc()

        if Buttons.any_pressed():
            bus.emit('button.pressed.{0}'.format(Buttons.pressed_str()))
        else:
            display.render_events(event_manager)

        sleep(0.125)

