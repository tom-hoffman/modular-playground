import board            # helps set up pins, etc. on the board
import digitalio        # digital (on/off) output to pins, including board LED.
import neopixel         # controls the RGB LEDs on the board

# below from https://docs.circuitpython.org/en/latest/shared-bindings/supervisor/index.html
_TICKS_PERIOD = const(1<<29)
_TICKS_MAX = const(_TICKS_PERIOD-1)
_TICKS_HALFPERIOD = const(_TICKS_PERIOD//2)

def ticks_diff(ticks1, ticks2):
    "Compute the signed difference between two ticks values, assuming that they are within 2**28 ticks"
    diff = (ticks1 - ticks2) & _TICKS_MAX
    diff = ((diff + _TICKS_HALFPERIOD) & _TICKS_MAX) - _TICKS_HALFPERIOD
    return diff

def ticks_less(ticks1, ticks2):
    "Return true if ticks1 is less than ticks2, assuming that they are within 2**28 ticks"
    return ticks_diff(ticks1, ticks2) < 0

class Debouncer(object):

    def __init__(self, b, current_value=None):
        self.b = b
        if current_value is None:
            self.current_value = b.value
        else:
            self.current_value = current_value

    def went_down(self):
        new = self.b.value
        changed = new and (not self.current_value)
        self.current_value = new
        return changed
        
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT
led.value = True


a_button_raw = digitalio.DigitalInOut(board.BUTTON_A)
a_button_raw.direction = digitalio.Direction.INPUT
a_button_raw.pull = digitalio.Pull.DOWN
a_button = Debouncer(a_button_raw)

b_button_raw = digitalio.DigitalInOut(board.BUTTON_B)
b_button_raw.direction = digitalio.Direction.INPUT
b_button_raw.pull = digitalio.Pull.DOWN
b_button = Debouncer(b_button_raw)

switch = digitalio.DigitalInOut(board.SLIDE_SWITCH)
switch.direction = digitalio.Direction.INPUT
switch.pull = digitalio.Pull.UP

def switch_is_left():
    return switch.value

pix = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=0.2, auto_write=False)