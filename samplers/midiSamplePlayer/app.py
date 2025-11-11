import gc
import os

from audiocore import WaveFile

import cpx
from minimal_midi import MinimalMidi

gc.collect()
print("Free bytes app.py after imports = " + str(gc.mem_free()))

BANKS = ("kick", "snare", "perc")
BANK_COLORS = ((0, 0, 16), (16, 0, 0), (0, 16, 0))

class SamplePlayerApp(object):
    def __init__(self, channel, note):
        self.channel = channel
        self.note = note
        self.sampleIndex = 0
        self.bankIndex = 0
        self.wav_file = None
        self.wav = None
        self.midi = MinimalMidi(channel, None)
    
    def changeSample(self):
        path = BANKS[self.bankIndex] + '/' + str(self.sampleIndex)
        fileName = os.listdir(path)[0]
        self.wav_file = open(path + '/' + fileName, 'rb')
        self.wav = WaveFile(self.wav_file)
        
    def updatePixels(self):
        pass
        
    def checkButtons(self):
        pass
        
    def main(self):
        self.changeSample()
        self.updatePixels()
        self.midi.clear_msgs()
        while True:
            self.checkButtons()
            msg = self.midi.get_msg()
            if msg is not None:
                if msg['type'] == 'NoteOn':
                    if msg['note'] == self.note:
                        cpx.audio.play(self.wav)
                        cpx.led.value = not cpx.led.value
gc.collect()
print("Free bytes app.py after imports = " + str(gc.mem_free()))
