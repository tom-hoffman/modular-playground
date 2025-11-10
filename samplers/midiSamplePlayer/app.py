import os

from audiocore import WaveFile

import cpx

BANKS = ("kick", "snare", "perc")
BANK_COLORS = ((0, 0, 16), (16, 0, 0), (0, 16, 0))

class SamplePlayerApp(object):
    def __init__(self, channel, note):
        self.channel = channel
        self.note = note
        self.noteOn = generateNoteOnValue(self.channel)
        self.sampleIndex = 0
        self.bankIndex = 0
        self.wav_file = None
        self.wav = None
    
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
        while True:
            self.checkButtons()
            msg = self.get_msg()
            if msg == b'\x90': #ch0
                cpx.audio.play(self.wav)
                cpx.led.value = not led.value
