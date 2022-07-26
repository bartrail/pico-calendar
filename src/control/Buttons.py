from machine import Pin

class Button:
    name: str
    pin: Pin

    def __init__(self, name, pin):
        self.name = name
        self.pin = pin

class Buttons:

    list = [
        Button('a', Pin(15, Pin.IN, Pin.PULL_UP)),
        Button('b', Pin(17, Pin.IN, Pin.PULL_UP)),
        Button('up', Pin(2, Pin.IN, Pin.PULL_UP)),
        Button('down', Pin(18, Pin.IN, Pin.PULL_UP)),
        Button('left', Pin(16, Pin.IN, Pin.PULL_UP)),
        Button('right', Pin(20, Pin.IN, Pin.PULL_UP)),
        Button('center', Pin(3, Pin.IN, Pin.PULL_UP)),
    ]

    @staticmethod
    def pressed() -> [str]:
        pressed = []
        for button in Buttons.list:

            if button.pin.value() == 0:
                pressed.append(button.name)

        return pressed

    @staticmethod
    def pressed_str() -> str:
        return '.'.join(Buttons.pressed())

    @staticmethod
    def any_pressed() -> bool:
        return len(Buttons.pressed()) > 0

