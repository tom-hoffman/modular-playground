import gc
import os

from audiocore import WaveFile    

from cpx import led, a_button, b_button, switch, switchIsLeft, pix, innie, outie, audio, spkrenable

BANKS = ("kick", "snare", "perc")
BANK_COLORS = ((0, 0, 16), (16, 0, 0), (0, 16, 0))

def generateNoteOnValue(channel):
    return int.to_bytes(0b10010000 | channel)

class SamplePlayerApp(object):
    def __init__(self, channel, note):
        self.channel = channel
        self.noteOn = generateNoteOnValue(self.channel)
        print(self.noteOn)
        self.note = note
        self.sampleIndex = 0
        self.bankIndex = 0
        self.wav_file = None
        self.wav = None



    def changeSample(self):
        path = BANKS[self.bankIndex] + '/' + str(self.sampleIndex)
        fileName = os.listdir(path)[0]
        self.wav_file = open(path + '/' + fileName, 'rb')
        self.wav = WaveFile(self.wav_file)

    def checkButtons(self):
        a_button.update()
        b_button.update()
        if a_button.rose:
            self.bankIndex = (self.bankIndex + 1) % 3
            self.changeSample()
            self.updatePixels()
        if b_button.rose:
            self.sampleIndex = (self.sampleIndex + 1) % 10
            self.changeSample()
            self.updatePixels()

    def get_msg(self):
        return innie.read(1)

    def updateBackground(self):
        pix.fill(BANK_COLORS[self.bankIndex])

    def updateSelector(self):
        pix[self.sampleIndex] = (32, 32, 32)

    def updatePixels(self):
        self.updateBackground()
        self.updateSelector()
        pix.show()

    def main(self):
        self.changeSample()
        self.updatePixels()
        while True:
            self.checkButtons()
            msg = self.get_msg()
            if msg == b'\x9f':
                audio.play(self.wav)
                led.value = not led.value
