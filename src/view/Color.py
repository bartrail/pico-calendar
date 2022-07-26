class Color:
    blue = 0xF800
    red = 0x07E0
    green = 0x001F

    yellow = 0x07FF
    magenta = 0xFFE0
    cyan = 0xF81F
    black = 0x0000
    white = 0xffff

    orange = 0x8C31 # correct ?

    @staticmethod
    def get(name):
        return getattr(Color, name)