
from app import SequencePlayerApp
from util import *

class ActivePlayer(SequencePlayerApp):

    def process_MIDI(self):
        prev_pitch = self.pitch
        if self.msg['type'] == "Clock":
            if self.clockCount >= self.duration - 1:
                self.clockCount = 0
                #cpx.led.value = not(cpx.led.value)
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
                    self.playing = False 
            else:
                self.clockCount = self.clockCount + 1
                if self.playing:
                    self.midi.send_note_off(self.pitch)
                    self.playing = False
            return ActivePlayer(self.notes, 
                                self.midi.out_channel,
                                self.tuneIndex,
                                self.clockCount,
                                self.noteIndex,
                                self.tune,
                                self.pitch,
                                self.duration,
                                self.playing)
        else:
            return self
