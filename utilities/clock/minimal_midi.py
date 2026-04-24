# minimal_midi.py
# Please note that this file is not a complete library but a
# template for a customized MIDI handling module. 
# CircuitPython on a CPX is both memory constrained and slow
# for real time MIDI processing on a busy MIDI network.  
# Customize the main loop in particular to process needed 
# messages as quickly as possible. 

# Note that MinimalMidi uses 0-15 numbering for MIDI channels.
# Your MIDI device may display channels as 1-16,
# thus you may need to subtract 1 from the displayed value
# to match the value here.

import usb_midi

from micropython import const

_CLOCK = const(b'\xF8')
_START = const(b'\xFA')
_STOP = const(b'\xFC')

# These "ports" are not to be confused with MIDI channels, etc.
_OUTIE = usb_midi.ports[1]

class MinimalMidi(object):
    """Tightly implementing the subset of MIDI we need."""
    
    def send_clock(self):
        _OUTIE.write(_CLOCK)
    
    def send_start(self):
        _OUTIE.write(_START)
    
    def send_stop(self):
        _OUTIE.write(_STOP)
