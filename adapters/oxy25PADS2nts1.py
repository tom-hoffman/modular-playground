# Oxygen25 ***PADS*** -> NTS-1 MIDI Adapter PADS
# MIDI IN (from Oxygen25 ***PADS***) 
# MIDI OUT (to NTS-1) 
# The pads (on our Oxygen25) are mapped to a different channel than
# the keys and other controls.  We're using them as buttons that send
# CC codes, so this is adapting both the channel and message type.

import gc
gc.collect()
print("Starting free bytes (after gc) = " + str(gc.mem_free()))
import board
import digitalio

import usb_midi
import adafruit_midi

from adafruit_midi.control_change import ControlChange
from adafruit_midi.note_on import NoteOn

gc.collect()
print("Free bytes after imports = " + str(gc.mem_free()))

gc.collect()
print("Free bytes after setup = " + str(gc.mem_free()))

CONTROLLER_OUT = 0x09
TARGET_IN = 0x00

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

# Note that the in/out PORTS are always 0 & 1 for USB.
# "Ports" are not MIDI channels.
midi = adafruit_midi.MIDI(midi_in = usb_midi.ports[0],
                          midi_out = usb_midi.ports[1],
                          in_channel = CONTROLLER_OUT,
                          out_channel = TARGET_IN)

osc_value = 0

def rollover(n):
    if n > 124:
        return 0
    else:
        return n

while True:
    msg_in = midi.receive()
    if isinstance(msg_in, NoteOn):
        # pad 5 -> oscillator
        if msg_in.note == 50: 
            osc_value = rollover(osc_value + 25)
            midi.send(ControlChange(53, osc_value))
        
        
'''
drumPads = {36 : DrumPad('OSC TYPE', 0, 25), -- cc53
            38 : DrumPad('FILTER TYPE', 0, 18), -- cc42
            42 : DrumPad('EG TYPE', 0, 25), -- cc14
            46 : DrumPad('DELAY TYPE', 0, 21), -- cc89
            50 : DrumPad('REVERB TYPE', 0, 21)} -- cc90
            mod -- cc88
            arp -- cc117

'''
    
