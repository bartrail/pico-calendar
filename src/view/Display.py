from machine import Pin, PWM

import config
from src.model.Date import Date
from src.model.Event import Event
from src.ical.EventManager import EventManager
from src.view.Color import Color
from src.view.LCDScreen import LCDScreen
from src.wifi import network_status


class Display:
    lcd: LCDScreen

    offset_left = 2
    offset_top = 2

    lines = {}

    def __init__(self):
        BL = 13
        pwm = PWM(Pin(BL))
        pwm.freq(1000)
        pwm.duty_u16(32768)  # max 65535

        self.lcd = LCDScreen()

        for l in range(0, 20):
            self.lines[l] = l * 10 + self.offset_top

        self.render_idle()


    def __show(self):
        self.lcd.show()

    def __text(self, text, left, top, color):
        if config.DEBUG:
            print(text)
        self.lcd.text(text, left, top, color)

    def __text_line(self, text, line, color):
        self.__text(text, self.offset_left, self.lines[line], color)

    def render_idle(self):
        self.lcd.fill(Color.blue)
        self.__show()

    def render_connecting(self, wlan, status: int):
        self.lcd.fill(Color.white)
        self.__text_line('Wifi Connecting to {0}: {1}'.format(config.WIFI_SSID, status), 0, Color.blue)
        self.__text_line('{0}'.format(network_status[str(status)]), 1, Color.blue)
        self.__show()

    def render_wifi_status(self, wifi):
        if wifi.status() != 3:
            self.__render_wifi_error(wifi)
        else:
            self.__render_wifi_success(wifi)

        self.__show()

    def __render_wifi_success(self, wifi):
        status = wifi.ifconfig()
        self.lcd.fill(Color.white)
        self.__text_line('Connected to {0}'.format(config.WIFI_SSID), 0, Color.blue)
        self.__text_line('IP: {0}'.format(status[0]), 1, Color.blue)

    def __render_wifi_error(self, wifi):
        status = wifi.status()
        self.lcd.fill(Color.red)
        self.__text_line('Connection Error to {0}'.format(config.WIFI_SSID), 0, Color.white)
        self.__text_line('Error: {0}'.format(network_status[str(status)]), 1, Color.white)

    def render_events_loaded(self, em: 'EventManager'):
        self.lcd.fill(Color.white)
        self.__text_line('Loaded {0} events'.format(len(em.events)), 0, Color.blue)

        self.__text_line('First Event: {0} at {1}'.format(
            em.first_event().summary,
            em.first_event().date_start.iso8601
        ), 1, Color.blue)

        self.__text_line('Last Event: {0} at {1}'.format(
            em.last_event().summary,
            em.last_event().date_start.iso8601
        ), 2, Color.blue)

    def render_current_time(self, em: 'EventManager'):
        self.lcd.fill(Color.white)
        self.__text_line(em.now.iso8601, 0, Color.blue)
        self.__show()
