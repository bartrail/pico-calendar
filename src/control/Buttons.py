from machine import Pin


class Buttons:

    buttons = {
        'a' : Pin(15, Pin.IN, Pin.PULL_UP),
        'b' : Pin(17, Pin.IN, Pin.PULL_UP),
        'up': Pin(2, Pin.IN, Pin.PULL_UP),
        'down' : Pin(18, Pin.IN, Pin.PULL_UP),
        'left' : Pin(16, Pin.IN, Pin.PULL_UP),
        'right' : Pin(20, Pin.IN, Pin.PULL_UP),
        'center' : Pin(3, Pin.IN, Pin.PULL_UP)
    }

    @staticmethod
    def pressed() -> [str]:
        pressed = []
        for b in Buttons.buttons:
            button = Buttons.buttons[b]

            if button.value() == 0:
                pressed.append(b)

        return pressed

    @staticmethod
    def any_pressed() -> bool:
        return len(Buttons.pressed()) > 0
