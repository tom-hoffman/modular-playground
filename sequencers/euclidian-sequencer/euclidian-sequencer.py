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
from adafruit_midi.timing_clock import TimingClock
from adafruit_midi.start import Start
from adafruit_midi.stop import Stop
#from adafruit_midi.midi_continue import Continue

if DEV_MODE:
    gc.collect()
    print("Free bytes after imports = " + str(gc.mem_free()))

############

# CONSTANTS
LED_COUNT = 10
MAX_VELOCITY = 5
DEFAULT_VELOCITY = 4
NOTE_COUNT = 4
NOTES = [36, 38, 59, 47]

############

# variables

channel_out = 1

############

# board setup steps

# set up the red LED

a_button = digitalio.DigitalInOut(board.BUTTON_A)
a_button.direction = digitalio.Direction.INPUT
a_button.pull = digitalio.Pull.DOWN

b_button = digitalio.DigitalInOut(board.BUTTON_B)
b_button.direction = digitalio.Direction.INPUT
b_button.pull = digitalio.Pull.DOWN

switch = digitalio.DigitalInOut(board.SLIDE_SWITCH)
switch.direction = digitalio.Direction.INPUT
switch.pull = digitalio.Pull.UP

def switchIsLeft():
    return switch.value

midi = adafruit_midi.MIDI(midi_in = usb_midi.ports[0],
                          midi_out = usb_midi.ports[1],
                          out_channel = channel_out)

pix = neopixel.NeoPixel(board.NEOPIXEL, 10)
pix.fill((255, 0, 255))
pix.show()

if DEV_MODE:
    gc.collect()
    print("Free bytes after board setup = " + str(gc.mem_free()))


############
# Objects

class EuclidianSequencer(object):
    
    def __init__(self):
        self.steps = 9
        self.triggers = 2
        self.active_step = 8
        self.sequence = []
        self.active_step = 0

    def update(self):
        '''
        Generates a "Euclidian rhythm" where triggers are
        evenly distributed over a given number of steps.
        Takes in a number of triggers and steps, 
        returns a list of Booleans.
        Based on Jeff Holtzkener's Javascript implementation at
        https://medium.com/code-music-noise/euclidean-rhythms-391d879494df
        '''
        slope = self.triggers / self.steps
        result = []
        previous = None
        for i in range(self.steps):
            # adding 0.0001 to correct for imprecise math in CircuitPython.
            current = math.floor((i * slope) + 0.001) 
            result.append(current != previous)
            previous = current
        self.sequence = result
        return self  # so you can do method chaining.

    def addStep(self):
        if self.steps < 10:
            self.steps += 1
        else:
            self.steps = 1
            self.triggers = 0
            self.active_step = 0
        self.update()
    
class SequencerApp(object):
    def __init__(self, sequence):
        self.seq = sequence
        self.a = a_button.value
        self.b = b_button.value
        self.switchIsLeft = switch.value
        self.note_index = 0
        self.velocity_index = 4
        self.started = False
        self.starting_step = 0

    def getRed(self, i):
        if i == self.seq.active_step:
            return 64
        else:
            return 0

    def getGreen(self, i):
        if self.seq.sequence[i]:
            return 48
        else:
            return 0

    def getBlue(self, i):
        # add velocity calculation
        return 16

    def updateSequenceDisplay(self):
        for i in range(LED_COUNT):
            if i < len(self.seq.sequence):
                pix[i] = (self.getRed(i), self.getGreen(i), self.getBlue(i))
            else:
                pix[i] = (0, 0, 0)
            
    def updateConfigDisplay(self):
        pix.fill((8, 8, 8))
    
    def updateNeoPixels(self):
        if switchIsLeft():
            self.updateConfigDisplay()
        else:
            self.updateSequenceDisplay()
        pix.show

    def addTrigger(self):
        pass

    def checkSwitch(self):
        # Return value indicates if NeoPixels need to be updated.
        if self.switchIsLeft != switch.value:
            self.switchIsLeft = switch.value
            return True
        else:
            return False

    def checkA(self):
        # Return value indicates if NeoPixels need to be updated.
        update = False
        if self.a != a_button.value:
            if a_button.value:
                self.seq.addStep()
                update = True
            self.a = a_button.value
        return update
            
    def main(self):
        while True:
            # These method calls change state and return True or False.
            # True indicates we need to call updateNeoPixels()
            if (self.checkSwitch() or self.checkA()):
                self.updateNeoPixels()
            msg_in = midi.receive()
            if msg_in:
                # if there is a message flip the red led
                led.value = not(led.value)


app = SequencerApp(EuclidianSequencer().update())
app.updateNeoPixels()

if DEV_MODE:
    gc.collect()
    print("Free bytes after object def and creation = " + str(gc.mem_free()))

app.main()
