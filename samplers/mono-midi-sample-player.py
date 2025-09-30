# Modular Playground Monophonic Sample Player
# Copyright 2025 Tom Hoffman
# License: MIT

# Plays one sample, interrupting and restarting on new NoteOn.
# Ignores the note value, just triggers on any NoteOn to the channel.

# The starting point of this file was:
# https://github.com/adafruit/Adafruit_Learning_System_Guides/blob/main/Introducing_CircuitPlaygroundExpress/CircuitPlaygroundExpress_AudioFiles/code.py
# SPDX-FileCopyrightText: 2017 Limor Fried for Adafruit Industries
# SPDX-License-Identifier: MIT

# We use the gc library to check and manage available RAM during development
import gc
gc.collect()
print("Starting free bytes (after gc) = " + str(gc.mem_free()))

import board            # helps set up pins, etc. on the board
import digitalio        # digital (on/off) output to pins
import neopixel         # controls the RGB LEDs on the board

import usb_midi         # basic MIDI over USB support
import adafruit_midi    # additional MIDI helpers from Adafruit

from adafruit_midi.note_on import NoteOn    # the specific messages we need 
from adafruit_midi.note_off import NoteOff

from audioio import AudioOut                # lets us play audio 
from audiocore import WaveFile              # lets us use .wav files


gc.collect()
print("Free bytes after imports = " + str(gc.mem_free()))

# COLORS

NOTE_ON_COLOR = (32, 0, 32)
NOTE_OFF_COLOR = (16, 16, 0)

# MIDI setup

doNoteLoop = False

# The controller sending note messages is set to send on this channel:

channel_in = 0

# wav = "rimshot.wav"
WAV_LIST = ["rimshot.wav"]

# Enable the speaker

spkrenable = digitalio.DigitalInOut(board.SPEAKER_ENABLE)
spkrenable.direction = digitalio.Direction.OUTPUT
spkrenable.value = True

# set up the red LED

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT
led.value = True


# Note that the in/out "ports" are always 0 & 1 for USB.
# "Ports" are not MIDI channels.
midi = adafruit_midi.MIDI(midi_in = usb_midi.ports[0],
                          midi_out = usb_midi.ports[1],
                          in_channel = channel_in)

neoPixels = neopixel.NeoPixel(board.NEOPIXEL, 10)

gc.collect()
print("Free bytes after setup = " + str(gc.mem_free()))

# These "with" statements are used to cleanly open and close 
# files, data streams and data outputs in Python.  
# They are called "context managers."

with open(WAV_LIST[0], "rb") as wf:                         # opens the wav
    with WaveFile(wf) as wave:                      # loads it for playback
        with AudioOut(board.SPEAKER) as audio:      # sets up the speaker 
            while True:                             # start main loop
                msg_in = midi.receive() 
                if msg_in:
                    print(type(msg_in))
                if isinstance(msg_in, NoteOn):
                    if msg_in.velocity == 0:   
                        audio.stop()                    # stop note if playing
                        neoPixels.fill(NOTE_OFF_COLOR)
                    else:   # if it is a NoteOn
                        audio.play(wave)                # play from beginning
                        neoPixels.fill(NOTE_ON_COLOR)   
                elif (isinstance(msg_in, NoteOff) and doNoteLoop):
                    audio.stop()                    # stop note if playing
                    neoPixels.fill(NOTE_OFF_COLOR)
                elif msg_in:                        # flash LED for other msg
                    led.value = not(led.value)
