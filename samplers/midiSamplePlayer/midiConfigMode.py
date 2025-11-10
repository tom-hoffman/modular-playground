import cpx
from binaryCounter import displayByte

print("Starting...")

RED = (16, 0, 0)
GREEN = (0, 16, 0)
BLUE = (0, 0, 16)
CYAN = (0, 16, 16)
PURPLE = (16, 0, 16)
YELLOW = (16, 16, 0)
WHITE = (16, 16, 16)
BLACK = (0, 0, 0)
OFF = BLACK

class ModeBaseClass(object):
    '''This will have your additional attributes, methods, etc.'''
    def __init__(self, channel, note):
        self.channel = channel
        self.note = note

class MidiConfigMode(ModeBaseClass):
    
    def updateNoteDisplay(self):
        displayByte(self.note, RED, BLUE, cpx.pix)
        cpx.pix.show()
    
    def updateChannelDisplay(self):
        displayByte(self.channel, YELLOW, PURPLE, cpx.pix)
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


b = MidiConfigMode(1, 60)

b.updatePixels()
cpx.pix.show()

while True:
    cpx.a_button.update()
    cpx.b_button.update()
    cpx.switch.update()
    b.checkButtons()
    if (cpx.switch.rose or cpx.switch.fell):
        b.updatePixels()

