# SPDX-FileCopyrightText: 2025 Tom Hoffman & E-Cubed students
# SPDX-License-Identifier: MIT

# Modular Playground Simple MIDI Sequencer

# Module Description:
# Sends a pre-defined sequence of MIDI notes.

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
from adafruit_midi.note_on import NoteOn    
# from adafruit_midi.note_off import NoteOff
from adafruit_midi.timing_clock import TimingClock
from adafruit_midi.midi_message import note_parser

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
channel_out = 15

NOTES2 = (('G4', '8dn'),
         ('G4', '16n'),
         
         ('A4', '4n'),
         ('G4', '4n'),
         ('C5', '4n'),
         
         ('B4', '4n'),
         ('G4', '8dn'),
         ('G4', '16n'),
         
         ('A4', '4n'), 
         ('G4', '4n'),
         ('D5', '4n'),
         
         ('C5', '2n'),
         ('G4', '8dn'),
         ('G4', '16n'),
         
         ('G5', '4n'),
         ('E5', '4n'),
         ('C5', '4n'),
         
         ('B4', '4n'),
         ('A4', '4n'),
         ('F5', '8dn'),
         ('F5', '16n'),
         
         ('E5','4n'),
         ('C5','4n'),  
         ('D5','4n'),
         ('C5', '2n'),
         ('C1', '2n'),
         ('C1', '1n'))

NOTES = ( ('F#3', '4n'),
          ('C#3', '4n'),
          ('E3', '4n'),
          ('F3', '4n'),
          ('E3', '4n'),
          ('C3', '4n'),
          ('B2', '4n'),
          ('C3', '4n'))

NOTE_DURATIONS = {'32n' : 3,
                  '16n' : 6,
                  '8n' : 12,
                  '4n' : 24,
                  '2n' : 48,
                  '1n' : 96,
                  '1dn' : 144,
                  '2dn' : 72,
                  '4dn' : 36,
                  '8dn' : 18}

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

# functionDefinitions
# Use camelCase for function definitions:
# First letter lower case, first letter of new words upper case.

def getNotePair(index):
    # Returns (pitch, duration) from the notes tuple.
    return NOTES[index]

def getPitch(index):
    note_pair = getNotePair(index)
    pitch_text = note_pair[0]
    return note_parser(pitch_text)

def getDuration(index):
    note_pair = getNotePair(index)
    note_text = note_pair[1]
    return NOTE_DURATIONS[note_text]


# starting variables for main loop
clockCount = 0
noteIndex = 0
pitch = getPitch(noteIndex)
duration = getDuration(noteIndex)

############
# Main loop(s)
while True:
    # try to get a midi message
    msg_in = midi.receive() 
    # if there is a new message
    if msg_in:
        # and if it is a clock message
        if isinstance(msg_in, TimingClock):
            # if we've completed the count for the current duration
            # move to the next note
            if clockCount >= duration - 1:
                # reset the clock counter
                clockCount = 0
                # flip the red led
                led.value = not(led.value)
                # add to the noteIndex, looping back to 0 if necessary
                noteIndex = noteIndex + 1
                if noteIndex >= len(NOTES):
                    noteIndex = 0
                # get new note values
                pitch = getPitch(noteIndex)
                duration = getDuration(noteIndex)
                midi.send(NoteOn(pitch, 127))
            else:
                clockCount = clockCount + 1 
