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
# Playing: plays notes on and off, processes clock, stop changes mode.
# Stopped: only waits for start or continue
# * start from beginning
# * continue from where you left off
# Skipping: waiting for end of message



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

# Messages we're using:
_CLOCK = const(0xF80)
_START = const(0xFA)

# Messages we're specifically NOT using and filtering out.
_ACTIVE_SENSING = const(0xFE)
_PITCH_BEND_NYBBLE = const(0b1110)

innie = usb_midi.ports[0]
outie = usb_midi.ports[1]

def isStatusByte(b):
    '''This returns true if this is the first part of a status message.'''
    return b >> 7 & 1

def isSystemMessage(b):
    return (b >> 4) == 15

def getChannel(b):
    return b & 0b00001111  

def quickDrop(msg):
    '''Dropping specific messages we are not using but may flood the input.'''
    return ((msg == _ACTIVE_SENSING) or (msg >> 4 == _PITCH_BEND_NYBBLE))

def channelDrop(b, channels):
    # if it is a system level message we won't drop it here
    if isSystemMessage(b):
        return False
    else:
        # if we aren't listening on any channel drop channel level messages
        if channels is None:
            return True
        else:
            # return true if this isn't a channel we're listening to
            return getChannel() not in channels  

class MiniMidi():
    def __init__(self, in_channels=None, out_channels=None):
        # add some guards
        self.in_channels = in_channels    # None or tuple of valid channel numbers
        self.out_channels = out_channels  # None or tuple of valid channel numbers
        self.status = "playing"  # "playing", "stopped", "skipping"
                
    def get_msg(self):
        # read one byte
        raw = (innie.read(1))
        # if we didn't get an empty byte
        if raw != b'':
            # convert the byte type to a number
            b = ord(raw)
            # quickly some dropping messages we definitely don't need to use (yet)
            if quickDrop(b) or channelDrop(b, self.in_channel):  
                return None
            if self.status != "stopped":
                # if we are not stopped, process clock.
                if b == _CLOCK:
                    return {'msg' : 'clock'}
            else:
                self.status = "playing"
                if dev_mode:  print("Now playing...")
                return {'msg' : 'start'}
            # check channel.
            
            # do note on/off
            # stop/start/continue
  
        else:  # if we got an empty byte
            return None       

midi = MiniMidi()

if DEV_MODE:
    gc.collect()
    print("Free bytes after setup = " + str(gc.mem_free()))

while True:
    midi.get_msg()

