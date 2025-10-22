# SPDX-FileCopyrightText: 2025 Tom Hoffman
# SPDX-License-Identifier: MIT

# MiniMidi.py
# WIP description:
# MiniMidi will be a minimalist MIDI library aimed at highly memory constrained 
# CircuitPython devices, specifically the Adafruit Circuit Playground Express.
# The program flow is structured around the patterns of MIDI binary encoding,
# in such a way that might make sense to an intermediate high school programmer.

DEV_MODE = True

# We use the gc library to check and manage available RAM during development
if DEV_MODE:
    import gc
    gc.collect()
    print("Starting free bytes (after gc) = " + str(gc.mem_free()))

import usb_midi         # basic MIDI over USB support

if DEV_MODE:
    gc.collect()
    print("Free bytes after imports = " + str(gc.mem_free()))

innie = usb_midi.ports[0]
outie = usb_midi.ports[1]

class MiniMidi():
    
    def __init__(self, in_channel, out_channel):
        self.in_channel = in_channel & 0b1111    # one 4 bit nybble
        self.out_channel = out_channel & 0b1111  # one 4 bit nybble

    def dropHighBit(self, n):
        # n is a number
        return n & 0b01111111
    
    def isSystemRealTime(self, d):
        return d['low'] & 0b1000
    
    def isSystemMessage(self, d):
        return d['high'] == 0b1111

    def isMessage(self, n):
        # n is a number
        return n & 0b10000000

    def isData(self, n):
        return not self.isMessage(n)

    def isInputChannel(self, n):
        return n == self.in_channel

    def processSystemExclusive(self, d):
        pass

    def processQuarterFrame(self, d):
        pass

    def processSongPosition(self, d):
        pass 

    def processSongSelect(self, d):
        pass

    REAL_TIME_MESSAGES = ("Timing Clock", "Undefined", "Start", "Continue",
                         "Stop", "Undefined", "Active Sensing", "Reset")
    
    def processSystemRealTime(self, d):
        m = d['low'] & 0b0111
        return {'msg' : self.REAL_TIME_MESSAGES[m]}
            
    def processSystemCommon(self, d):
        m = d['low'] & 0b0111
        if m == 0b000:
            return self.processSystemExclusive(d)
        elif m == 0b001:
            return self.processQuarterFrame(d)
        elif m == 0b010:
            return self.processSongPosition(d)
        elif m == 0b011:
            return self.processSongSelect(d)
        elif (m == 0b100) or (m == 0b101):
            raise RuntimeError("Undefined system common message.")
        elif m == 0b110:
            return {'msg' : 'Tune Request'}
        elif m == 0b111:
            raise RuntimeError("End of SysEx without beginning of SysEx.")
        else:
            raise RuntimeError("Error parsing system common message.")

    def processSystemMessage(self, d):
        if self.isSystemRealTime(d):
            return self.processSystemRealTime(d)
        else:
            return self.processSystemCommon(d)

    def processNote(self, d, msg):
        k = self.getByte()
        v = self.getByte()
        if self.isData(k) and self.isData(v):
            return {'msg' : msg, 
                    'note' : self.dropHighBit(k),
                    'velocity' : self.dropHighBit(v)}
        else:
            raise RuntimeError("Message byte when expecting data byte.")

    def processControlChange(self, d):
        return None

    def processProgramChange(self, d):
        return None
    
    def processChannelPressure(self, d):
        return None
    
    def processPitchBend(self, d):
        return None

    def processChannelMessage(self, d):
        if self.isInputChannel(d['low']):
            m = d['high'] & 0b0111
            if m == 0b000:
                return self.processNote(d, "Note Off")
            elif m == 0b001:
                return self.processNote(d, "Note On")
            elif m == 0b010:
                return self.processNote(d, "Polyphonic Key Pressure")
            elif m == 0b011:
                return self.processControlChange(d)
            elif m == 0b100:
                return self.processProgramChange(d)
            elif m == 0b101:
                return self.processChannelPressure(d)
            elif m == 0b110:
                return self.processPitchBend(d)
            else:
                raise RuntimeError("Error processing Channel Message")
        else:
            return None         

    def processMessage(self, d):
        if self.isSystemMessage(d):
            return self.processSystemMessage(d)
        else:
            return self.processChannelMessage(d)
    
    def processMessageByte(self, b):
        # b is a number
        d = {'high' : b >> 4, 'low' : b & 0b00001111}  
        if self.isMessage(b):
            return self.processMessage(d)
        else:
            raise RuntimeError("Not a message byte at beginning of message.")
    
    def getByte(self):
        raw = innie.read(1)
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
            return self.processMessageByte(b)    

midi = MiniMidi(0, 15)

if DEV_MODE:
    gc.collect()
    print("Free bytes after setup = " + str(gc.mem_free()))

while True:
    m = midi.get_msg() 
    if m is not None:
        print(m)
