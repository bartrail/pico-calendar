from machine import Pin, PWM

import config
from src.model.Date import Date
from src.model.Event import Event
from src.wifi import Wifi
from src.ical.EventManager import EventManager
from src.view.Color import Color
from src.view.LCDScreen import LCDScreen


class Display:
    lcd: LCDScreen

    offset_x = 2
    offset_y = 2

    lines = {}

    def __init__(self):
        BL = 13
        pwm = PWM(Pin(BL))
        pwm.freq(1000)
        pwm.duty_u16(32768)  # max 65535

        self.lcd = LCDScreen()

        for l in range(0, 20):
            self.lines[l] = l * 10 + self.offset_y

        self.render_idle()


    def __show(self):
        self.lcd.show()

    def __text(self, text, left, top, color):
        if config.DEBUG:
            print(text)
        self.lcd.text(text, left, top, color)

    def __text_line(self, text, line, color):
        self.__text(text, self.offset_x, self.lines[line], color)

    def render_idle(self):
        self.lcd.fill(Color.black)
        self.__show()

    def render_connecting(self, wifi: 'Wifi'):
        self.lcd.fill(Color.white)
        self.__text_line('Wifi Connecting to {0}: {1}'.format(wifi.ssid, wifi.status()), 0, Color.blue)
        self.__text_line('{0}'.format(wifi.status_str()), 1, Color.blue)
        self.__show()

    def render_wifi_status(self, wifi: 'Wifi'):
        if wifi.status() != 3:
            self.__render_wifi_error(wifi)
        else:
            self.__render_wifi_success(wifi)

        self.__show()

    def __render_wifi_success(self, wifi: 'Wifi'):
        self.lcd.fill(Color.white)
        self.__text_line('Connected to {0}'.format(wifi.ssid), 0, Color.blue)
        self.__text_line('IP: {0}'.format(wifi.ip()), 1, Color.blue)

    def __render_wifi_error(self, wifi: 'Wifi'):
        self.lcd.fill(Color.red)
        self.__text_line('Connection Error to {0}'.format(wifi.ssid), 0, Color.white)
        self.__text_line('Error: {0}'.format(wifi.status_str()), 1, Color.white)

    def render_loading_data(self):
        self.lcd.fill(Color.white)
        self.__text_line('Loading Data...', 0, Color.blue)
        self.__show()

    def render_error(self, message, error: 'BaseException'):
        self.lcd.fill(Color.red)
        self.__text_line(message, 0, Color.white)
        self.__text_line('Type: {0}'.format(error), 2, Color.white)
        self.__show()

    def render_events_loaded(self, em: 'EventManager'):
        self.lcd.fill(Color.white)

        self.__text_line(em.now.iso8601, 0, Color.blue)

        for idx, event in enumerate(em.events):
            self.__text_line('{0}: {1}'.format(
                event.summary,
                event.date_start.iso8601
            ), idx + 1, Color.blue)

        self.__show()

    def render_current_time(self, em: 'EventManager'):
        self.lcd.fill(Color.white)
        self.__text_line(em.now.iso8601, 0, Color.blue)
        self.__show()

    def render_events(self, em: 'EventManager'):
        if not em.has_events_today() and not em.has_events_tomorrow():
            self.render_idle()
            return


        if em.has_events_today() and not em.has_events_tomorrow():

            self.__render_single_event(em.get_events_of_today()[0])

            return

        if not em.has_events_today() and em.has_events_tomorrow():

            return

    def __render_single_event(self, event: 'Event'):
        self.lcd.fill(Color.white)
        self.__text_line(event.date_start.iso8601, 0, Color.blue)
        self.__text_line(event.summary, 1, Color.blue)

        if event.summary in config.EVENT_MAP:
            color = Color.get(config.EVENT_MAP[event.summary])
        else:
            color = Color.black

        self.lcd.fill_rect(
            self.offset_x,
            22,
            self.lcd.width - self.offset_y * 2,
            self.lcd.height - 20 - self.offset_y * 2,
            color
        )
        self.__show()