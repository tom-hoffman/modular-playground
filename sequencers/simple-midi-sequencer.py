# SPDX-FileCopyrightText: 2025 Tom Hoffman & E-Cubed students
# SPDX-License-Identifier: MIT

# Modular Playground Simple MIDI Sequencer

# Module Description:# SPDX-FileCopyrightText: 2025 Tom Hoffman & E-Cubed students
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

NOTES = (('G3', '8dn'),
         ('G3', '16n'),
         ('A3', '4n'),
         ('G3', '4n'),
         ('C3', '4n'),
         ('B3', '4n'),
         ('G3', '8dn'),
         ('G3', '16n'),
         ('A3', '4n'), 
         ('G3', '4n'),
         ('D3', '4n'),
         ('C3', '2n'),
         ('G3', '8dn'),
         ('G3', '16n'),
         ('G3', '4n'),
         ('E4', '4n'),
         ('C3', '4n'),
         ('B3', '4n'),
         ('A3', '4n'),
         ('F3', '8dn'),
         ('F3', '16n'),
         ('E3','4n'),
         ('D3','4n'),  
         ('C3','4n'),
         ('D0', '1n'))

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
    msg_in = midi.receive() 
    if msg_in:
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
channel_out = 15

notes = (('G3', '8dn'),
         ('G3', '16n'),
         ('A4', '4n'),
         ('G3', '4n'),
         ('C4', '4n'),
         ('B4', 'dn'),
         ('G3', '8dn'),
         ('G3', '16n'),
         ('A4', '4n'), 
         ('G3', '4n'),
         ('D4', '4n'),
         ('C4', '2n'),
         ('G3', '8dn'),
         ('G3', '16n'),
         ('G3', '4n'),
         ('E4', '4n'),
         ('C4', '4n'),
         ('B4', '4n'),
         ('A4', '4n'),
         ('F3', '8dn'),
         ('F3', '16n'),
         ('E3','4n'),
         ('D4','4n'),  
         ('C4','4n'))

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

clockCount = 0
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



############
# Main loop(s)
currentIndex = 0
current_pitch = note_parser(notes[currentIndex][0])
current_duration = NOTE_DURATIONS[notes[currentIndex][1]]
print(current_duration)
activeNote = currentIndex
while True:
    msg_in = midi.receive() 
    if msg_in:
        if isinstance(msg_in, TimingClock):
            if clockCount == 23:
                # if there is a message flip the red led
                led.value = not(led.value)
                clockCount = 0
                midi.send(NoteOn(notes[activeNote] - 12, 127))
                activeNote = activeNote + 1
                if activeNote >= len(notes):
                    activeNote = 0
            clockCount = clockCount + 1 
