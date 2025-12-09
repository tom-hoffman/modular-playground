from app import SequencePlayerApp
from util import *

class ActivePlayer(SequencePlayerApp):

    def process_MIDI(self):
        if self.msg['type'] == "Clock":
            if self.clockCount >= self.duration - 1:
                self.clockCount = 0
                self.noteIndex = self.noteIndex + 1
                if self.noteIndex >= len(self.tune):
                    self.noteIndex = 0
                # make this a method is app.py
                self.send_note()

            else:
                self.clockCount = self.clockCount + 1
                if self.playing:
                    self.midi.send_note_off(self.pitch)
                    self.playing = False
            return ActivePlayer(self.notes, 
                                self.midi,
                                self.tuneIndex,
                                self.tune,
                                self.clockCount,
                                self.noteIndex,
                                self.pitch,
                                self.duration,
                                self.playing)
        else:
            return self
