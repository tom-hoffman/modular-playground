import cpx
import midi_modes

_RED = (8, 0, 0)
_GREEN = (0, 255, 0)
_BLUE = (0, 0, 255)
_CYAN = (0, 16, 16)
_PURPLE = (6, 0, 6)
_YELLOW = (64, 64, 0)
_WHITE = (32, 32, 32)
_ORANGE = (32, 16, 0)
_BLACK = (0, 0, 0)
_OFF = _BLACK

class View(object):

    def __init__(self, led=cpx.led):
        self.led = led
    
    def toggle_led(self):
        self.led.value = not(self.led.value)
    
    def get_mode_color(self, mode):
        if mode == 'sustaining':
            return _YELLOW
        elif mode == 'counting':
            return _PURPLE
        elif mode == 'stopped':
            return _RED
        else:
            return _ORANGE

class SelectorView(View):

    def update_pixels(self, i, mode_string):
        c = self.get_mode_color(mode_string)
        cpx.pix.fill(c)
        cpx.pix[i] = _WHITE
        cpx.pix.show()
    
