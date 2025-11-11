# Sets up the standard hardware we need for Modular Playground applications.

import board            # helps set up pins, etc. on the board
import digitalio        # digital (on/off) output to pins, including board LED.
import neopixel         # controls the RGB LEDs on the board
import audioio

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

switch_raw = digitalio.DigitalInOut(board.SLIDE_SWITCH)
switch_raw.direction = digitalio.Direction.INPUT
switch_raw.pull = digitalio.Pull.UP
switch = Debouncer(switch_raw)

def switchIsLeft():
    return switch.value

pix = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=0.2, auto_write=False)

audio = audioio.AudioOut(board.A0)

spkrenable = digitalio.DigitalInOut(board.SPEAKER_ENABLE)
spkrenable.direction = digitalio.Direction.OUTPUT
spkrenable.value = True
