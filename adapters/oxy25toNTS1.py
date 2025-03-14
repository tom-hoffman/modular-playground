# Oxygen25 -> NTS-1 MIDI Adapter
# MIDI IN (from Oxygen25) 
# MIDI OUT (to NTS-1) 

import gc
gc.collect()
print("Starting free bytes (after gc) = " + str(gc.mem_free()))
import board
import digitalio

import usb_midi
import adafruit_midi

from adafruit_midi.control_change import ControlChange
from adafruit_midi.note_off import NoteOff
from adafruit_midi.note_on import NoteOn
from adafruit_midi.pitch_bend import PitchBend

gc.collect()
print("Free bytes after imports = " + str(gc.mem_free()))

CONTROLLER_OUT = 0x0E
TARGET_IN = 0x00

# For the NTS-1 {effect description : MIDI Control Change number}
def buildCCMap():
    TARGET_CODES = {
        'EG TYPE' : 14,
        'ATTACK' : 16,
        'RELEASE' : 19,
        'TREMOLO DEPTH' : 20,
        'TREMOLO RATE' : 21,
        'LFO RATE' : 24,
        'LFO DEPTH' : 26,
        'MOD TIME' : 28,
        'MOD DEPTH' : 29,
        'DELAY TIME' : 30,
        'DELAY DEPTH' : 31,
        'DELAY MIX' : 33,
        'REVERB TIME' : 34,
        'REVERB DEPTH' : 35,
        'REVERB MIX' : 36,
        'FILTER TYPE' : 42,
        'FILTER CUTOFF' : 43,
        'FILTER RESONANCE' : 44,
        'FILTER SWEEP DEPTH' : 45,
        'FILTER SWEEP RATE' : 46,
        'OSC TYPE' : 88,
        'DELAY TYPE' : 89,
        'REVERB TYPE' : 90,
        'ARP PATTERN' : 117,
        'ARP INTERVALS' : 118,
        'ARP LENGTH' : 119
    }

    # for the Oxygen25 CC KNOBS (not pads or keyboard)
    # {Control ID on device : MIDI Control Change Number}
    CONTROLLER_CODES = {
        # Control Knobs
        'C1' : 74,
        'C2' : 71,
        'C3' : 91,
        'C4' : 93,
        'C5' : 73,
        'C6' : 72,
        'C7' : 5,
        'C8' : 84,
    
    # slider
    'C9' : 7,
    # C10 button, sends value 0
    # nb: C10 also sends value 0 to CC number 0???
    'C10' : 32, 
    # C11 - C14 send 127 on down, 0 on up.
    # repeat button
    'C11' : 113,
    # stop button
    'C12' : 116,
    # play button
    'C13' : 117,
    # record button
    'C14' : 118,
    # C15 = pitch wheel, no CC
    # MOD wheel
    'C16' : 1
    }
    
    # This is the human readable mapping.
    # {CONTROLLER_CODES key : TARGET_CODES key}    
    CC_STRING_MAPPING = {
        'C16' : 'FILTER CUTOFF',
        'C1'  : 'ARP PATTERN',
        'C5'  : 'ARP INTERVALS',
        'C2'  : 'ARP LENGTH',
        'C8'  : 'FILTER RESONANCE',
        'C6'  : 'REVERB TYPE'
        }
    ccMap = {}
    for controller_id in CC_STRING_MAPPING.keys():
        ccMap[CONTROLLER_CODES[controller_id]] = \
            TARGET_CODES[CC_STRING_MAPPING[controller_id]]
    return ccMap

CC_MAP = buildCCMap()
gc.collect()

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

# Note that the in/out PORTS are always 0 & 1 for USB.
# "Ports" are not MIDI channels.
midi = adafruit_midi.MIDI(midi_in = usb_midi.ports[0],
                          midi_out = usb_midi.ports[1],
                          in_channel = CONTROLLER_OUT,
                          out_channel = TARGET_IN)

def handleNoteOn(m):
    midi.send(NoteOn(m.note, m.velocity))
    led.value = not(led.value)

def handleControlChange(m):
    try:
        midi.send(ControlChange(CC_MAP[m.control], m.value)) 
    except:
        print(f"No mapping defined for CC number {m.control}.")

def handlePitchBend(m):
    midi.send(PitchBend(m.pitch_bend))
    pass

def handleNoteOff(m):
    midi.send(NoteOff(m.note))

gc.collect()
print("Free bytes after setup = " + str(gc.mem_free()))

while True:
    msg_in = midi.receive()
    if isinstance(msg_in, NoteOn):
        handleNoteOn(msg_in)
    elif isinstance(msg_in, ControlChange):
        handleControlChange(msg_in)
    elif isinstance(msg_in, PitchBend):
        handlePitchBend(msg_in)
    elif isinstance(msg_in, NoteOff):
        handleNoteOff(msg_in)


    
