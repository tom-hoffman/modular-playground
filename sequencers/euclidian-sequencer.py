# SPDX-FileCopyrightText: 2025 Tom Hoffman
# SPDX-License-Identifier: MIT

# Modular Playground MIDI Application Template

# Module Description:
# Starting boilerplate for Modular Playground MIDI applications.

# Put gc.mem_free() checks and other print statements inside
# conditionals which will only run when DEV_MODE is True.
# Code will run faster with DEV_MODE set to False.
# Before release, you can delete those code blocks for better performance.
DEV_MODE = True

# We use the gc library to check and manage available RAM during development
if DEV_MODE:
    import gc
    gc.collect()
    print("Starting free bytes (after gc) = " + str(gc.mem_free()))

import math             # need the floor function
import board            # helps set up pins, etc. on the board
import digitalio        # digital (on/off) output to pins, including board LED.
import neopixel         # controls the RGB LEDs on the board

import usb_midi         # basic MIDI over USB support
# adafruit_midi must be copied to /lib directory on CPX.
import adafruit_midi    # additional MIDI helpers from Adafruit

from adafruit_midi.note_on import NoteOn    
from adafruit_midi.note_off import NoteOff
from adafruit_midi.timing_clock import TimingClock
from adafruit_midi.start import Start
from adafruit_midi.stop import Stop
from adafruit_midi.midi_continue import Continue

if DEV_MODE:
    gc.collect()
    print("Free bytes after imports = " + str(gc.mem_free()))

############

# CONSTANTS
LED_COUNT = 10
MAX_VELOCITY = 5
DEFAULT_VELOCITY = 4
NOTE_COUNT = 4
NOTES[4] = {36, 38, 59, 47}

# COLORS
# Delete the ones you don't need.
# Add others as needed!

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
PURPLE = (255, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
OFF = BLACK

############

# variables

channel_out = 1

############

# board setup steps

# set up the red LED
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT
led.value = True

midi = adafruit_midi.MIDI(midi_in = usb_midi.ports[0],
                          midi_out = usb_midi.ports[1],
                          out_channel = channel_out)

neoPixels = neopixel.NeoPixel(board.NEOPIXEL, 10)

if DEV_MODE:
    gc.collect()
    print("Free bytes after setup = " + str(gc.mem_free()))

############

# functionDefinitions

def generateEuclidian(triggers, steps):
    '''
    Generates a "Euclidian rhythm" where triggers are
    evenly distributed over a given number of steps.
    Takes in a number of triggers and steps, 
    returns a list of Booleans.
    Based on Jeff Holtzkener's Javascript implementation at
    https://medium.com/code-music-noise/euclidean-rhythms-391d879494df
    '''
    slope = triggers / steps
    print(slope)
    result = []
    previous = None
    for i in range(steps):
        # adding 0.0001 to correct for imprecise math in CircuitPython.
        current = math.floor((i * slope) + 0.001) 
        result.append(current != previous)
        previous = current
    return result

############
# Main loop(s)

while True:
    msg_in = midi.receive()
    if msg_in:
        # if there is a message flip the red led
        led.value = not(led.value)







