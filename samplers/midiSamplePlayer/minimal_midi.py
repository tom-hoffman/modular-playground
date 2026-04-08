# minimal_midi.py
# Please note that this file is not a complete library but a
# template for a customized MIDI handling module. 
# CircuitPython on a CPX is both memory constrained and slow
# for real time MIDI processing on a busy MIDI network.  
# Customize the main loop in particular to process needed 
# messages as quickly as possible.

# Note that MinimalMidi uses 0-15 numbering for MIDI channels.
# Your MIDI device may display channels as 1-15,
# thus you may need to subtract 1 from the displayed value
# to match the value here.

# MIDI inputs -> NoteOn, optional CC.
# MIDI outputs -> none.

import usb_midi

from micropython import const

import config

_NOTE_ON_NYBBLE = const(0b1001) << 4
_FOUR_BIT_MASK = const(0b1111)

# These "ports" are not to be confused with MIDI channels, etc.
_INNIE = usb_midi.ports[0]

def note_on_value(ch: int):
    return ch | _NOTE_ON_NYBBLE

class MinimalMidi(object):
    """Tightly implementing the subset of MIDI we need."""
    def __init__(self, in_channel):
        self.in_channel = in_channel & _FOUR_BIT_MASK
        self.note_on_value = note_on_value(self.in_channel)

    def clear_msgs(self):
        m = _INNIE.read(1)
        while m:
            m = _INNIE.read(1)
    
    def process_note(self, m):
        n = ord(_INNIE.read(1))
        v = ord(_INNIE.read(1))
        return {'type' : m, 'note' : n, 'velocity' : v}
    
    def process_channel_msg(self, n):
        left = (n >> 4)
        if left == _NOTE_ON_NYBBLE:
            return self.process_note('NoteOn')
        elif left == _NOTE_OFF_NYBBLE:
            return self.process_note('NoteOff')   
        else:
            return None
    
    def get_msg(self):
        m = _INNIE.read(1)              # grab a byte
                                        # processing single byte messages
        if m == b'':                    # drop empty bytes
            return None
        else:
            n = ord(m)                  # convert to an integer
        if n == :     # ditch stray data bytes quickly
            return None


        #if (n & 0b1111) == self.in_channel:
        #    return self.process_channel_msg(n)
        else:
            return None
        



    





    

