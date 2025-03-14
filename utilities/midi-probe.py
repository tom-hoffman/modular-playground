# Allows you to send incremental values to a CC control number using
# Circuit Playground buttons and USB-MIDI.

from adafruit_circuitplayground import cp

import usb_midi
import adafruit_midi

from adafruit_midi.control_change import ControlChange


count = 0
Astate = False
Bstate = False

TARGET_IN = 0x00

# OSC: SAW 0-24, TR1 25-49, SQR 50-74, UPN 75-99, VALUE 100-127
# EG: ASDR 0-24, AHr 25-49, Ar 50-74, Ar LooP 75-99, OPEN 100-127
# FILTER: LP 2 0-17, LP 4 18-35, BP 2 36-53, BP 4 54-71, HP 2 72-89, HP 4 90-107 OFF 108-127
# DELAY: OFF 0-20, STEREO 21-41, MONO 42-62, PING PONG 63-83, HIGHPASS 84-104, TAPE 105-127
# REVERB: OFF 0-20, HALL 21-41, PLATE 42-62, SPACE 63-83, RISER 84-104. SUBMARINE 105-127
# MOD: OFF 0-24, CHORUS 25-49, ENSEMBLE 50-74, PHASER 75-99, FLANGER 100-127

# Note that the in/out PORTS are always 0 & 1 for USB.
# "Ports" are not MIDI channels.
midi = adafruit_midi.MIDI(midi_in = usb_midi.ports[0],

                          midi_out = usb_midi.ports[1],
                          in_channel = 0,
                          out_channel = TARGET_IN)

# This is the ControlChange number you are testing.
TESTING = 88

while True:
    if cp.button_b:
        if not(Bstate):
            count = count + 1
            Bstate = True
            print(count)
            midi.send(ControlChange(TESTING, count)) 
    else:
        Bstate = False
        
    if cp.button_a:
        if not(Astate):
            count = count - 1
            Astate = True
            print(count)
            midi.send(ControlChange(TESTING, count)) 
    else:
        Astate = False
