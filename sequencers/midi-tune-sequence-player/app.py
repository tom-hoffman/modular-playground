import usb_midi         # basic MIDI over USB support
import adafruit_midi    # additional MIDI helpers from Adafruit

# Uncomment only the message types you must read or send.
# You can delete the rest. These are just the most commonly used messages.
from adafruit_midi.note_on import NoteOn    
from adafruit_midi.note_off import NoteOff
from adafruit_midi.timing_clock import TimingClock
from adafruit_midi.midi_message import note_parser

import cpx

NOTE_DURATIONS = {'32n' : 3,
                  '16n' : 6,
                  '8n' : 12,
                  '4n' : 24,
                  '2n' : 48,
                  '1n' : 96,
                  '1dn' : 144,
                  '2dn' : 72,
                  '4dn' : 36,
                  '8dn' : 18}

midi = adafruit_midi.MIDI(midi_in = usb_midi.ports[0],
                          midi_out = usb_midi.ports[1],
                          in_channel = 0,
                          out_channel = 15)

def getTune(notes, index):
    return notes[index]

def getNotePair(tune, index):
    # Returns (pitch, duration) from the notes tuple.
    return tune[index]

def getPitch(tune, index):
    note_pair = getNotePair(tune, index)
    pitch_text = note_pair[0]
    return note_parser(pitch_text)

def getDuration(tune, index):
    note_pair = getNotePair(tune, index)
    note_text = note_pair[1]
    return NOTE_DURATIONS[note_text]

class SequencePlayerApp(object):
    def __init__(self, notes):
        self.notes = notes
        self.tuneIndex = 0
        self.clockCount = 0
        self.noteIndex = 0
        self.tune = getTune(self.notes, self.tuneIndex)
        self.pitch = getPitch(self.tune, self.noteIndex)
        self.duration = getDuration(self.tune, self.noteIndex)
        self.playing = False

    def updatePixels(self):
        cpx.pix.fill((32, 0, 32))
        cpx.pix[self.tuneIndex] = (0, 32, 0)
        cpx.pix.show()

    def updateTune(self):
        self.noteIndex = 0
        self.clockCount = 0
        self.tune = getTune(self.notes, self.tuneIndex)
        self.pitch = getPitch(self.tune, self.noteIndex)
        self.duration = getDuration(self.tune, self.noteIndex)
        self.playing = False
        self.updatePixels()

    def checkButtons(self):
        cpx.a_button.update()
        cpx.b_button.update()
        if cpx.a_button.rose:
            self.tuneIndex -= 1
        if cpx.b_button.rose:
            self.tuneIndex += 1

    def main(self):
        self.updatePixels()
        while True:
            msg_in = midi.receive() 
            if msg_in:
                self.checkButtons()
                if isinstance(msg_in, TimingClock):
                    if self.clockCount >= self.duration - 1:
                        self.clockCount = 0
                        cpx.led.value = not(cpx.led.value)
                        self.noteIndex = self.noteIndex + 1
                        if self.noteIndex >= len(self.tune):
                            self.noteIndex = 0
                        self.pitch = getPitch(self.tune, self.noteIndex)             
                        if self.pitch:
                            self.duration = getDuration(self.tune, self.noteIndex)
                            midi.send(NoteOn(self.pitch, 127))
                            self.playing = True
                        else:
                            midi.send(NoteOff(self.pitch, 0))
                    else:
                        self.clockCount = self.clockCount + 1
                        if self.playing:
                            print("HAI")
                            midi.send(NoteOff(self.pitch, 0))
                            self.playing = False
