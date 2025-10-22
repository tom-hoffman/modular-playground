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
        self.in_channel = in_channel & 0b1111    # one 4 bit number
        self.out_channel = out_channel & 0b1111  # one 4 bit number

    def dropHighBit(self, n):
        # n is a number
        return n & 0b01111111
    
    def isSystemRealTime(self, d):
        return d['low'] & 0b0100
    
    def isSystemMessage(self, d):
        return d['high'] == 0b1111

    def isMessage(self, n):
        # n is a number
        return n & 0b10000000

    def isData(self, n):
        return not isMessage(n)

    def isInputChannel(self, n):
        return m == self.innie

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
        if DEV_MODE:
            print(self.REAL_TIME_MESSAGES(m))
        return {'msg' : self.REAL_TIME_MESSAGES(m)}
            
    def processSystemCommon(self, d):
        m = d['low'] & 0b0111
        if m == 0b000:
            if DEV_MODE:
                print("System Exclusive")
            return self.processSystemExclusive(d)
        elif m == 0b001:
            if DEV_MODE:
                print("Quarter Frame")
            return self.processQuarterFrame(d)
        elif m == 0b010:
            if DEV_MODE:
                print("Song Position Pointer")
        elif m == 0b011:
            if DEV_MODE:
                print("Song Select")
        elif (m == 0b100) or (m == b0101):
            raise RuntimeError("Undefined system common message.")
        elif m == 0b110:
            if DEV_MODE:
                print("Tune Request")
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
                    'note' : dropHighBit(k),
                    'velocity' : dropHighBit(v)}
        else:
            raise RuntimeError("Message byte when expecting data byte.")

    def processChannelMessage(d):
        if self.isInputChannel(d['low']):
            m = d['high'] & 0b01110000
            if m == 0b000:
                if DEV_MODE:
                    print("Note Off")
                return self.processNote(d, "Note Off")
            elif m == 0b001:
                if DEV_MODE:
                    print("Note On")
                return self.processNote(d, "Note On")
            elif m == 0b010:
                if DEV_MODE:
                    print("Polyphonic Key Pressure")
                return self.processNote(d, "Polyphonic Key Pressure")
            elif m == 0b011:
                if DEV_MODE:
                    print("Control Change")
                return self.processControlChange(d)
            elif m == 0b100:
                if DEV_MODE:
                    print("Program Change")
                return self.processProgramChange(d)
            elif m == 0b101:
                if DEV_MODE:
                    print("Channel Pressure")
                return self.processChannelPressure(d)
            elif m == 0b110:
                if DEV_MODE:
                    print("Pitch Bend")
                return self.processPitchBend(d)
            
        else:
            if DEV_MODE:
                print("Not the selected input channel.")
            return None         

    def processMessage(self, d):
        if self.isSystemMessage(d):
            return self.processSystemCommon(d)
        else:
            return self.processChannelMessage(d)
    
    def processMessageByte(self, b):
        # b is a number
        d = {'high' : b & 0b11110000, 'low' : b & 0b00001111}  
        if self.isMessage(b):
            return self.processMessage(d)
        else:
            raise RuntimeError("Not a message byte at beginning of message.")
    
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
