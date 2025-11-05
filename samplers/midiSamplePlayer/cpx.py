import board            # helps set up pins, etc. on the board
import digitalio        # digital (on/off) output to pins, including board LED.
import neopixel         # controls the RGB LEDs on the board

import usb_midi         # basic MIDI over USB support

from adafruit_debouncer import Debouncer

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

def switchIsLeft():
    return switch.value

pix = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=0.2, auto_write=True)
pix.brightness = 0.2
pix.fill((255, 0, 255))
pix.show()

innie = usb_midi.ports[0]
outie = usb_midi.ports[1]

audio = AudioOut(board.A0)
