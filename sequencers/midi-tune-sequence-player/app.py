import cpx
from minimal_midi import MinimalMidi
from util import NOTE_DURATIONS, note_parser

def getTune(notes, index):
    return notes[index]

def getNotePair(tune, index):
    # Returns (pitch, duration) from the notes tuple.
    return tune[index]

def getPitch(tune, index):
    note_pair = getNotePair(tune, index)
    pitch_text = note_pair[0]
    print(pitch_text)
    return note_parser(pitch_text) 

def getDuration(tune, index):
    note_pair = getNotePair(tune, index)
    note_text = note_pair[1]
    return NOTE_DURATIONS[note_text]

class SequencePlayerApp(object):
    def __init__(self, notes, midi_out):
        self.notes = notes
        self.midi = MinimalMidi(None, midi_out)
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

    def check_buttons(self):
        changed = False
        cpx.a_button.update()
        cpx.b_button.update()
        if cpx.a_button.rose:
            self.tuneIndex -= 1
            changed = True
        if cpx.b_button.rose:
            self.tuneIndex += 1
            changed = True
        if changed:
            self.updatePixels()
            self.tune = getTune(self.notes, self.tuneIndex)
            self.noteIndex = 0
            self.clockCount = 0

    def process_MIDI(self):
        self.msg = self.midi.get_msg()
        prev_pitch = self.pitch
        if self.msg is not None:
            if self.msg['type'] == "Clock":
                if self.clockCount >= self.duration - 1:
                    self.clockCount = 0
                    cpx.led.value = not(cpx.led.value)
                    self.noteIndex = self.noteIndex + 1
                    if self.noteIndex >= len(self.tune):
                        self.noteIndex = 0
                    self.pitch = getPitch(self.tune, self.noteIndex)             
                    if self.pitch:
                        self.duration = getDuration(self.tune, self.noteIndex)
                        self.midi.send_note_on(self.pitch, 127)
                        self.playing = True
                    else:
                        self.midi.send_note_off(prev_pitch)
                        self.pitch = prev_pitch
                        
                else:
                    self.clockCount = self.clockCount + 1
                    if self.playing:
                        self.midi.send_note_off(self.pitch)
                        self.playing = False

