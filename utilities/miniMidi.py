# SPDX-FileCopyrightText: 2025 Tom Hoffman
# SPDX-License-Identifier: MIT

# MiniMidi.py
# WIP description:
# MiniMidi will be a minimalist MIDI library aimed at highly memory constrained 
# CircuitPython devices, specifically the Adafruit Circuit Playground Express.

# Supported messages:
# Note On
# Note Off
# Clock
# Start
# Stop
# Continue

# Modes:
# Playing: plays notes on and off, processes clock, start/stop change mode.
# Stopped: only waits for start or continue
# * start or continue


# notes on bytes
# to make bytes from hex numbers: bytes.fromhex('f8')
# reverse: aByte.hex()
# print binary: bin(ord(aByte))


DEV_MODE = True

# We use the gc library to check and manage available RAM during development
if DEV_MODE:
    import gc
    gc.collect()
    print("Starting free bytes (after gc) = " + str(gc.mem_free()))

from micropython import const

import board            # helps set up pins, etc. on the board
import digitalio        # digital (on/off) output to pins, including board LED.
import neopixel         # controls the RGB LEDs on the board

import usb_midi         # basic MIDI over USB support

if DEV_MODE:
    gc.collect()
    print("Free bytes after imports = " + str(gc.mem_free()))

# CONSTANTS

_CLOCK = bytes.fromhex('F8')

innie = usb_midi.ports[0]
outie = usb_midi.ports[1]

def isStatusByte(b):
    return b >> 7 & 1




class MiniMidi():
    def __init__(self, in_channel=(None), out_channel=(None)):

        self.in_channel = in_channel
        self.out_channel = out_channel
        self.status = "not started"
    
    def get_msg(self):
        raw = (innie.read(1))
        if raw != b'':
            b = ord(raw)
            if self.status == "not started":
                if b == 0xFA:
                    self.status = "started"
                    print("Starting...")
                    return {'msg' : 'start'}
                else:
                    return None
            
            

midi = MiniMidi()
while True:
    midi.get_msg()

