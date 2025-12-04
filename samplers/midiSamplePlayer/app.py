import os

from audiocore import WaveFile # type: ignore

import cpx
from minimal_midi import MinimalMidi # type: ignore

_BANKS = ("kick", "snare", "perc")


class SamplePlayerApp(object):

    
    def changeSample(self):
        path = _BANKS[self.bank_index] + '/' + str(self.sample_index)
        fileName = os.listdir(path)[0]
        self.wav_file = open(path + '/' + fileName, 'rb')
        self.wav = WaveFile(self.wav_file)

    def updateButtons(self):
        cpx.a_button.update()
        cpx.b_button.update()
        cpx.switch.update()

    def main(self):
        self.msg = self.midi.get_msg()
        if self.msg is not None:
            if self.msg['type'] == 'NoteOn':
                if self.msg['note'] == self.note:
                    cpx.audio.play(self.wav)
                    cpx.led.value = not cpx.led.value

