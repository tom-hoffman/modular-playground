# SPDX-FileCopyrightText: 2025 Tom Hoffman
# SPDX-License-Identifier: MIT

# MiniMidi.py
# WIP description:
# MiniMidi will be a minimalist MIDI library aimed at highly memory constrained 
# CircuitPython devices, specifically the Adafruit Circuit Playground Express.
# The program flow is structured around the patterns of MIDI binary encoding.

DEV_MODE = True

# We use the gc library to check and manage available RAM during development
if DEV_MODE:
    import gc
    gc.collect()
    print("Starting free bytes (after gc) = " + str(gc.mem_free()))

from micropython import const

import usb_midi         # basic MIDI over USB support

if DEV_MODE:
    gc.collect()
    print("Free bytes after imports = " + str(gc.mem_free()))

# CONSTANTS

# Messages we're using:
_CLOCK = const(0xF80)
_START = const(0xFA)
_NOTE_ON_NYBBLE = const(0x1001)
_NOTE_OFF_NYBBLE = const(0x1000)

# Messages we're specifically NOT using and filtering out.
_ACTIVE_SENSING = const(0xFE)
_PITCH_BEND_NYBBLE = const(0b1110)

innie = usb_midi.ports[0]
outie = usb_midi.ports[1]
  

class MiniMidi():
    
    def __init__(self, in_channel, out_channel):
        self.in_channel = in_channel & 0b1111    # one 4 bit number
        self.out_channel = out_channel & 0b1111  # one 4 bit number

    def isSystemMessage(self, d):
        return d['high'] == 0b1111

    def isMessage(self, n):
        # n is the high nybble
        return n & 0b1000

    def processSystemMessage(d):
        m = d['low']
        if m == 0b0000:
            print("System Exclusive")
        elif m == 0b0001:
            print("Quarter Frame")
        elif m == 0b0010:
            print("Song Position Pointer")
        elif m == 0b0011:
            print("Song Select")
        elif (m == 0b0100) or (m == 0b0101):
            if DEV_MODE:
                print("Undefined")
            return {'msg' : 'Undefined'}
        elif m == 0b0110:
            if DEV_MODE:
                print("Tune Request")
            return {'msg' : 'Tune Request'}

    def processChannelMessage(d):
        pass

    def processMessage(self, d):
        if self.isSystemMessage(d):
            return self.processSystemMessage(d)
        else:
            return self.processChannelMessage(d)
    
    def processByte(self, b):
        # b is a number
        d = {'high' : b & 0b11110000, 'low' : b & 0b00001111}  
        if self.isMessage(d['high']):
            return self.processMessage(d)
        else:
            if DEV_MODE:
                print("Not a message byte.")
            return None
    
    def getByte(self):
        raw = innie.read()
        if raw != b'':
            # convert the byte type to a number
            return ord(raw)     
        else:
            return None
    
    def get_msg(self):
        b = self.getByte()
        if b is None:
            return None
        else:
            # pass on a dict of the high and low nybbles
            return processMessage(b)    

midi = MiniMidi(0, 15)

if DEV_MODE:
    gc.collect()
    print("Free bytes after setup = " + str(gc.mem_free()))

while True:
    midi.get_msg()
