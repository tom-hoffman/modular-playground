import cpx
import app

_BANK_COLORS = ((0, 0, 16), (16, 0, 0), (0, 16, 0))
_SELECTION_COOL = (16, 16, 16)


class SampleSelectMode(app.SamplePlayerApp):
    
    def updateBackground(self):
        cpx.pix.fill(_BANK_COLORS[self.bank_index])

    def updateSelection(self):
        cpx.pix[self.sample_index] = _SELECTION_COOL

    def updatePixels(self):
        self.updateBackground()
        self.updateSelection()
        cpx.pix.show()

    def checkButtons(self):
        changed = False
        if cpx.a_button.rose:
            self.bank_index = (self.bank_index + 1) % 3
            changed = True
        if cpx.b_button.rose:
            self.sample_index = (self.sample_index + 1) % 10
            changed = True
        if changed:
            self.changeSample()
            self.updatePixels()



