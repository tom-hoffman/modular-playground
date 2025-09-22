# Modular Playground Multiple/Monophonic Sample Player
# Copyright 2025 Tom Hoffman
# License: MIT

# Plays one of several samples, but only one at a time.

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
RED = (255, 0, 0)
ORANGE = (255, 127, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
INDIGO = (75, 0, 130)
VIOLET = (143, 0, 0)
BLACK = (0, 0, 0)
# need a few more...
NEOPIXELS = [RED, ORANGE, YELLOW, GREEN, BLUE, INDIGO, VIOLET]

# MIDI setup
# The controller sending note messages is set to this channel:
CONTROLLER_OUT = 0x0E # might display as 14 or 15 on device!

class Sound:
    '''Encapsulates data about a sound.'''
    def __init__(self, midi_note: int, wav_file: str, neo:int):
        self.midi_note = midi_note  # note which triggers the sample
        self.wav_file = wav_file    # file to be played
        self.neo = neo              # which neopixel and color index

sounds = [Sound(36, "laugh.wav", 0),
          Sound(38, "rimshot.wav", 1),
          Sound(59, "laugh.wav", 2),
          Sound(47, "rimshot.wav", 3)]

# Enable the speaker
spkrenable = digitalio.DigitalInOut(board.SPEAKER_ENABLE)
spkrenable.direction = digitalio.Direction.OUTPUT
spkrenable.value = True

# Make the 2 input buttons
buttonA = digitalio.DigitalInOut(board.BUTTON_A)
buttonA.direction = digitalio.Direction.INPUT
buttonA.pull = digitalio.Pull.DOWN

buttonB = digitalio.DigitalInOut(board.BUTTON_B)
buttonB.direction = digitalio.Direction.INPUT
buttonB.pull = digitalio.Pull.DOWN

# set up the red LED
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT
led.value = True

pixels = neopixel.NeoPixel(board.NEOPIXEL, 10)

def play_sound(s):
    print("Playing file: " + s.wav_file)
    pixels[s.neo] = NEOPIXELS[s.neo]
    wf = open(s.wav_file, "rb")
    with WaveFile(wf) as wave:
        with AudioOut(board.SPEAKER) as audio:
            audio.play(wave)
            while audio.playing:
                pass    # make this non-blocking
    print("Finished")
    pixels[s.neo] = BLACK

# Note that the in/out "ports" are always 0 & 1 for USB.
# "Ports" are not MIDI channels.
midi = adafruit_midi.MIDI(midi_in = usb_midi.ports[0],
                          midi_out = usb_midi.ports[1],
                          in_channel = CONTROLLER_OUT)

gc.collect()
print("Free bytes after setup = " + str(gc.mem_free()))

while True:
    msg_in = midi.receive()
    if msg_in:
        led.value = not(led.value)
    if isinstance(msg_in, NoteOn):
        for s in sounds:
            if msg_in.note == s.midi_note:
                play_sound(s)
    if buttonA.value:
        play_sound(sounds[0])
    if buttonB.value:
        play_sound(sounds[1])

