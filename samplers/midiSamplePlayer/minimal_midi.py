# Note that MinimalMidi uses 0-15 numbering for MIDI channels.
# Your MIDI device may display channels as 1-15,
# thus you may need to subtract 1 from the displayed value
# to match the value here.

import usb_midi

from micropython import const

_CLOCK = const(b'\xF8')

_NOTE_ON_NYBBLE = const(0b1001)
_NOTE_OFF_NYBBLE = const(0b1000)
_CHANNEL_NYBBLE_MASK = const(0b1111)

# These "ports" are not to be confused with MIDI channels, etc.
_INNIE = usb_midi.ports[0]
_OUTIE = usb_midi.ports[1]


# Generates NoteOn/NoteOff message values indexed for each channel
NOTE_ON_MESSAGES = bytes(range(144, 160))
NOTE_OFF_MESSAGES = bytes(range(128, 144))
ALL_CHANNELS = range(0, 15)

class MinimalMidi(object):
    """Tightly implementing the subset of MIDI we need."""
    def __init__(self, in_channel, out_channel):
        self.in_channel = in_channel
        self.out_channel = out_channel

    def send_note_on(self, n, v):
        msgByte = NOTE_ON_MESSAGES[self.in_Channel]
        OUTIE.write(bytes([msgByte, n, v]))

    def send_note_off(self, n):
        msgByte = NOTE_OFF_MESSAGES[self.in_channel]
        _OUTIE.write(bytes([msgByte, n, 0]))
    
    def send_clock(self):
        _OUTIE.write(_CLOCK)

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
        m = _INNIE.read(1)
        # processing single byte messages
        if m == b'':
            return None
        elif m == _CLOCK:
            return {'type' : 'Clock'}
        else:
            n = ord(m) # continuing with n as integer
        if (n & 0b1111) == self.in_channel:
            return self.process_channel_msg(n)
        else:
            return None
        




    

