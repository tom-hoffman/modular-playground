import cpx
import app
from binary_counter import displayByte

_CYAN = (0, 16, 16)
_PURPLE = (16, 0, 16)
_YELLOW = (16, 16, 0)

class MidiConfigMode(app.SamplePlayerApp):
    
    def updateNoteDisplay(self):
        displayByte(self.note, _YELLOW, _CYAN, cpx.pix)
        cpx.pix.show()
    
    def updateChannelDisplay(self):
        displayByte(self.channel, _YELLOW, _PURPLE, cpx.pix)
        cpx.pix.show()
    
    def updatePixels(self):
        if cpx.switchIsLeft():
            self.updateChannelDisplay()
        else:
            self.updateNoteDisplay()

    def checkButtonsOnChannel(self):
        if cpx.a_button.rose:
            self.channel = self.channel - 1
            self.updateChannelDisplay()
        elif cpx.b_button.rose:
            self.channel = self.channel + 1
            self.updateChannelDisplay()

    def checkButtonsOnNote(self):
        if cpx.a_button.rose:
            self.note = self.note - 1
            self.updateNoteDisplay()
        elif cpx.b_button.rose:
            self.note = self.note + 1
            self.updateNoteDisplay()

    def checkButtons(self):
        if cpx.switchIsLeft():
            self.checkButtonsOnChannel()
        else:
            self.checkButtonsOnNote()


