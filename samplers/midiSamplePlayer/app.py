from cpx import led, a_button, b_button, switch, switchIsLeft, pix, innie, outie

BANKS = ("kick", "snare", "perc")


class SamplePlayerApp(object):
    def __init__(self):
        self.sampleIndex = 0
        self.bankIndex = 0

    def changeSample(self:
        pass

    def checkButtons(self):
        a_button.update()
        b_button.update()
        if a_button.rose:
            self.bankIndex = (self.bankIndex + 1) % 3
            self.changeSample()
        if b_button.rose:
            self.sampleIndex = (self.sampleIndex + 1) % 10
            self.changeSample()

    def main(self):
        while True:
            self.checkButtons()
            msg = self.get_msg()
           #if msg == _CLOCK_MSG:
