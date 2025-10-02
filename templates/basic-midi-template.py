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

import board            # helps set up pins, etc. on the board
import digitalio        # digital (on/off) output to pins, including board LED.
import neopixel         # controls the RGB LEDs on the board

import usb_midi         # basic MIDI over USB support
# adafruit_midi must be copied to /lib directory on CPX.
import adafruit_midi    # additional MIDI helpers from Adafruit

# Uncomment only the message types you must read or send.
# You can delete the rest. These are just the most commonly used messages.
#from adafruit_midi.note_on import NoteOn    
#from adafruit_midi.note_off import NoteOff
#from adafruit_midi.timing_clock import TimingClock
#from adafruit_midi.control_change import ControlChange
#from adafruit_midi.program_change import ProgramChange
#from adafruit_midi.system_exclusive import SystemExclusive

# if you need to output audio, uncomment the line below.
#from audioio import AudioOut
# if you need to read a .wav file, uncomment the line below.
# from audiocore import WaveFile

if DEV_MODE:
    gc.collect()
    print("Free bytes after imports = " + str(gc.mem_free()))

############

# CONSTANTS
# Use ALL_CAPS_WITH_UNDERSCORE for named values that do not change.

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
# use lower case with underscores for variables
# delete ones you don't need and add others

# listen for messages from:
channel_in = 0
# send messages on:
channel_out = 1

############

# board setup steps

# set up the red LED
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT
led.value = True

# Enable the speaker
# speaker = digitalio.DigitalInOut(board.SPEAKER_ENABLE)
# speaker.direction = digitalio.Direction.OUTPUT
# speaker.value = True

# Note that the in/out "ports" are always 0 & 1 for USB-<ODO.
# "Ports" are not MIDI channels.
midi = adafruit_midi.MIDI(midi_in = usb_midi.ports[0],
                          midi_out = usb_midi.ports[1],
                          in_channel = channel_in,
                          out_channel = channel_out)

neoPixels = neopixel.NeoPixel(board.NEOPIXEL, 10)

if DEV_MODE:
    gc.collect()
    print("Free bytes after setup = " + str(gc.mem_free()))

############

# Main loop(s)

while True:
    msg_in = midi.receive()
    if msg_in:
        # if there is a message flip the red led
        led.value = not(led.value)


# Main loop if you are playing samples:
# These "with" statements are used to cleanly open and close 
# files, data streams and data outputs in Python.
# You'll need to point it a real .wav file.  

#with open("example.wav", "rb") as wf:
#    with WaveFile(wf) as wave:                      # loads file for playback
#        with AudioOut(board.SPEAKER) as audio:      # sets up the speaker 
#            while True:                             # start main loop
#                msg_in = midi.receive() 
#                if msg_in:
#                    led.value = not(led.value)