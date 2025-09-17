# SPDX-FileCopyrightText: 2017 Limor Fried for Adafruit Industries
#
# SPDX-License-Identifier: MIT

import gc
gc.collect()
print("Starting free bytes (after gc) = " + str(gc.mem_free()))

import board
import digitalio

import usb_midi
import adafruit_midi

from adafruit_midi.note_on import NoteOn

from audiocore import WaveFile

from audioio import AudioOut

gc.collect()
print("Free bytes after imports = " + str(gc.mem_free()))

CONTROLLER_OUT = 0x0E
TARGET_IN = 0x00

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

# The two files assigned to buttons A & B
audiofiles = ["rimshot.wav", "laugh.wav"]

# set up the red LED
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

def play_file(filename):
    print("Playing file: " + filename)
    wave_file = open(filename, "rb")
    with WaveFile(wave_file) as wave:
        with AudioOut(board.SPEAKER) as audio:
            audio.play(wave)
            while audio.playing:
                pass
    print("Finished")

# Note that the in/out PORTS are always 0 & 1 for USB.
# "Ports" are not MIDI channels.
midi = adafruit_midi.MIDI(midi_in = usb_midi.ports[0],
                          midi_out = usb_midi.ports[1],
                          in_channel = CONTROLLER_OUT,
                          out_channel = TARGET_IN)

gc.collect()
print("Free bytes after setup = " + str(gc.mem_free()))

while True:
    msg_in = midi.receive()
    if isinstance(msg_in, NoteOn):
        play_file(audiofiles[0])
    if buttonA.value:
        play_file(audiofiles[0])
    if buttonB.value:
        play_file(audiofiles[1])

