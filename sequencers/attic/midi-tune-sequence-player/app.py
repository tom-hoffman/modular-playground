import cpx
from minimal_midi import MinimalMidi
from util import *



class SequencePlayerApp(object):
    def __init__(self, 
                 notes, 
                 midi,
                 tuneIndex = 0,
                 tune = None,
                 clockCount = 0,
                 noteIndex = 0,
                 pitch = None,
                 duration = None,
                 playing = False):
        self.notes = notes
        self.midi = midi
        self.tuneIndex = tuneIndex
        self.clockCount = clockCount
        self.noteIndex = noteIndex
        if tune is not None:
            self.tune = tune
        else:
            self.tune = getTune(self.notes, self.tuneIndex)
        if pitch is not None:
            self.pitch = pitch
        else:
            self.pitch = getPitch(self.tune, self.noteIndex)
        if duration is not None:
            self.duration = duration
        else:
            self.duration = getDuration(self.tune, self.noteIndex)
        self.playing = playing

    # add red led

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
            changed = False
    
    def get_MIDI(self):
        self.msg = self.midi.get_msg()
        return self.msg is not None

    def send_note(self):
        prev_pitch = self.pitch
        self.pitch = getPitch(self.tune, self.noteIndex)             
        if self.pitch:
            self.duration = getDuration(self.tune, self.noteIndex)
            self.midi.send_note_on(self.pitch, 127)
            self.playing = True
        else:
            self.midi.send_note_off(prev_pitch)
            self.pitch = prev_pitch
            self.playing = False 