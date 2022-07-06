from machine import Pin, PWM, ADC

from wifi import wifi_connect
from LCDScreen import LCDScreen
from ical.ApiClient import ApiClient
import config

BL = 13

sensor_temp = ADC(4)
conversion_factor = 3.3 / (65535)




def loadData():
        
    # file = open("ical.json", "r")
    # fileContent = file.read()
    
    Api = ApiClient(config.ICAL_URL)
    Api.parseResponse()

if __name__ == '__main__':

    led = Pin("LED", Pin.OUT)
    led.on()

    pwm = PWM(Pin(BL))
    pwm.freq(1000)
    pwm.duty_u16(32768)  # max 65535

    LCD = LCDScreen()

    # color BRG
    LCD.fill(LCD.white)

    reading = sensor_temp.read_u16() * conversion_factor
    temperature = 27 - (reading - 0.706) / 0.001721
    tempStr = '%.1f' % temperature

    offsetTop = 35
    offsetText = 15

    LCD.show()
    LCD.text("Raspi Pico", 90, offsetTop, LCD.red)
    LCD.text("PicoGo", 90, offsetTop + offsetText, LCD.green)
    LCD.text("Pico-LCD-1.14", 90, offsetTop + offsetText * 2, LCD.blue)
    LCD.text("Temp: " + tempStr + "C", 90, offsetTop + offsetText * 3, LCD.blue)

    # LCD.hline(10,10,220,LCD.blue)
    # LCD.hline(10,125,220,LCD.blue)
    # LCD.vline(10,10,115,LCD.blue)
    # LCD.vline(230,10,115,LCD.blue)

    LCD.show()
    keyA = Pin(15, Pin.IN, Pin.PULL_UP)
    keyB = Pin(17, Pin.IN, Pin.PULL_UP)

    keyUp = Pin(2, Pin.IN, Pin.PULL_UP)
    keyCtrl = Pin(3, Pin.IN, Pin.PULL_UP)
    keyLeft = Pin(16, Pin.IN, Pin.PULL_UP)
    keyDown = Pin(18, Pin.IN, Pin.PULL_UP)
    keyRight = Pin(20, Pin.IN, Pin.PULL_UP)

    try:
        wlan = wifi_connect(config.WIFI_SSID, config.WIFI_PASSWORD, config.WIFI_COUNTRY)
        wlan_status = wlan.ifconfig()
        LCD.text('{0} ({1})'.format(config.WIFI_SSID, wlan_status[0]), 2, 2, LCD.blue)
    except RuntimeError as err:
        LCD.text(str(err), 2, 2, LCD.red)
        wlan = False

    LCD.show()    
    loadData()


    while (1):

        if (keyA.value() == 0):
            LCD.fill_rect(208, 12, 20, 20, LCD.red)

            reading = sensor_temp.read_u16() * conversion_factor
            temperature = 27 - (reading - 0.706) / 0.001721
            tempStr = '%.1f' % temperature

            LCD.text("Temp: " + tempStr + "C", 90, offsetTop + offsetText * 3, LCD.blue)

            print("A")
        else:
            LCD.fill_rect(208, 12, 20, 20, LCD.white)
            LCD.rect(208, 12, 20, 20, LCD.red)

        if (keyB.value() == 0):
            LCD.fill_rect(208, 103, 20, 20, LCD.red)
            print("B")
        else:
            LCD.fill_rect(208, 103, 20, 20, LCD.white)
            LCD.rect(208, 103, 20, 20, LCD.red)

        if (keyUp.value() == 0):  # 上
            LCD.fill_rect(37, 35, 20, 20, LCD.red)
            print("UP")
        else:
            LCD.fill_rect(37, 35, 20, 20, LCD.white)
            LCD.rect(37, 35, 20, 20, LCD.red)

        if (keyCtrl.value() == 0):  # 中
            LCD.fill_rect(37, 60, 20, 20, LCD.red)
            print("CTRL")
        else:
            LCD.fill_rect(37, 60, 20, 20, LCD.white)
            LCD.rect(37, 60, 20, 20, LCD.red)

        if (keyLeft.value() == 0):  # 左
            LCD.fill_rect(12, 60, 20, 20, LCD.red)
            print("LEFT")
        else:
            LCD.fill_rect(12, 60, 20, 20, LCD.white)
            LCD.rect(12, 60, 20, 20, LCD.red)

        if (keyDown.value() == 0):  # 下
            LCD.fill_rect(37, 85, 20, 20, LCD.red)
            print("DOWN")
        else:
            LCD.fill_rect(37, 85, 20, 20, LCD.white)
            LCD.rect(37, 85, 20, 20, LCD.red)

        if (keyRight.value() == 0):  # 右
            LCD.fill_rect(62, 60, 20, 20, LCD.red)
            print("RIGHT")
        else:
            LCD.fill_rect(62, 60, 20, 20, LCD.white)
            LCD.rect(62, 60, 20, 20, LCD.red)

        LCD.show()

    time.sleep(1)
    LCD.fill(LCD.blue)
    LCD.show()
