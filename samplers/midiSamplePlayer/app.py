import os
import gc

from audiocore import WaveFile # type: ignore

import cpx
from minimal_midi import MinimalMidi # type: ignore

_BANKS = ("kick", "snare", "perc")


class SamplePlayerApp(object):
    def __init__(self, channel, note, sample_index=0, bank_index=0, 
                 wav_file=None, wav=None, midi=None):
        self.channel = channel
        self.note = note
        self.sample_index = sample_index
        self.bank_index = bank_index
        self.wav_file = wav_file
        self.wav = None
        self.midi = MinimalMidi(channel, None)
    
    def changeSample(self):
        gc.collect()
        #string.join?
        path = _BANKS[self.bank_index] + '/' + str(self.sample_index)
        fileName = os.listdir(path)[0]
        self.wav_file = open(path + '/' + fileName, 'rb')
        self.wav = WaveFile(self.wav_file)

    def updateButtons(self):
        cpx.a_button.update()
        cpx.b_button.update()
        cpx.switch.update()

    def main(self):
        _button_delay = 0
        while True:
            if _button_delay == 512:
                self.updateButtons() 
                self.checkButtons()
                _button_delay = 0
            else:
                _button_delay += 1
            msg = self.midi.get_msg()
            if msg is not None:
                if msg['type'] == 'NoteOn':
                    if msg['note'] == self.note:
                        cpx.audio.play(self.wav)
                        cpx.led.value = not cpx.led.value
                        print(gc.mem_free())

