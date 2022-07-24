from machine import Pin, PWM
from src.view.LCDScreen import LCDScreen

BL = 13


def draw_rainbow(lcd: 'LCDScreen'):
    color_steps_x = 65535 / lcd.width
    color_steps_y = 65535 / lcd.height

    color = 0

    LCD.fill(0x0000)

    for y in range(0, lcd.height):
        # color = color + 1
        for x in range(0, lcd.width):
            color = color + 1
            # print(x, color)
            # print(x, y, int(pricolor))

            lcd.pixel(x, y, int(color))

    lcd.show()


if __name__ == '__main__':
    led = Pin("LED", Pin.OUT)
    led.on()

    pwm = PWM(Pin(BL))
    pwm.freq(1000)
    pwm.duty_u16(32768)  # max 65535

    LCD = LCDScreen()
    draw_rainbow(LCD)
