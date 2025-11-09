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

INNIE = usb_midi.ports[0]
OUTIE = usb_midi.ports[1]


# Generates NoteOn/NoteOff message values indexed for each channel
NOTE_ON_MESSAGES = bytes(range(144, 160))
NOTE_OFF_MESSAGES = bytes(range(128, 144))
ALL_CHANNELS = range(0, 15)

class MinimalMidi(object):
    """Tightly implementing the subset of MIDI we need."""
    def __init__(self, inChannel, outChannel):
        # These "ports" are not to be confused with MIDI channels, etc.
        self.inChannel = inChannel
        self.outChannel = outChannel

    def sendNoteOn(self, n, v):
        msgByte = NOTE_ON_MESSAGES[self.inChannel]
        OUTIE.write(bytes([msgByte, n, v]))

    def sendNoteOff(self, n):
        msgByte = NOTE_OFF_MESSAGES[self.inChannel]
        OUTIE.write(bytes([msgByte, n, 0]))
    
    def sendClock(self):
        OUTIE.write(_CLOCK)

    def clear_msgs(self):
        m = INNIE.read(1)
        while m:
            m = INNIE.read(1)
    
    def processNote(self, m):
        n = ord(INNIE.read(1))
        v = ord(INNIE.read(1))
        return {'type' : m, 'note' : n, 'velocity' : v}
    
    def get_msg(self):
        m = INNIE.read(1)
        if m == b'':
            return None
        elif m == _CLOCK:
            return {'type' : 'Clock'}
        else:
            n = ord(m)
        left = (n >> 4)
        if left == _NOTE_ON_NYBBLE:
            return self.processNote('Note On')
        elif left == _NOTE_OFF_NYBBLE:
            return self.processNote('Note Off')

print("Starting...")
midi = MinimalMidi(1, 15)
midi.clear_msgs()
count = 0
while True:
    m = midi.get_msg()
    if m:
        print(m)
    midi.sendNoteOn(60, 127)
    midi.sendClock()
    midi.sendNoteOff(60)
    

