import board            # helps set up pins, etc. on the board
import digitalio        # digital (on/off) output to pins, including board LED.
import neopixel         # controls the RGB LEDs on the board

import usb_midi         # basic MIDI over USB support


# CONSTANTS

_CLOCK_MSG = const(0b11111000)

_LED_COUNT = const(10)
_CLOCK_LIMIT = const(24)  # for quarter note
_MAX_VELOCITY = const(5)
_DEFAULT_VELOCITY = const(4)
_NOTE_COUNT = const(4)
_NOTES = const((36, 38, 59, 47))
# board setup steps

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT
led.value = True

a_button = digitalio.DigitalInOut(board.BUTTON_A)
a_button.direction = digitalio.Direction.INPUT
a_button.pull = digitalio.Pull.DOWN

b_button = digitalio.DigitalInOut(board.BUTTON_B)
b_button.direction = digitalio.Direction.INPUT
b_button.pull = digitalio.Pull.DOWN

switch = digitalio.DigitalInOut(board.SLIDE_SWITCH)
switch.direction = digitalio.Direction.INPUT
switch.pull = digitalio.Pull.UP

def switchIsLeft():
    return switch.value

pix = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=0.2, auto_write=True)
pix.brightness = 0.2
pix.fill((255, 0, 255))
pix.show()

innie = usb_midi.ports[0]
outie = usb_midi.ports[1]

class SequencerApp(object):
    def __init__(self, sequence):
        self.seq = sequence
        self.a = a_button.value
        self.b = b_button.value
        self.switchIsLeft = switch.value
        self.note_index = 0
        self.velocity_index = 4
        self.started = False
        self.starting_step = 0
        self.clock_count = 0

    def getRed(self, i):
        if i == self.seq.active_step:
            return 64
        else:
            return 0

    def getGreen(self, i):
        if self.seq.sequence[i]:
            return 48
        else:
            return 0

    def getBlue(self, i):
        # add velocity calculation
        return 16

    def updateSequenceDisplay(self):
        for i in range(_LED_COUNT):
            if i < len(self.seq.sequence):
                pix[i] = (self.getRed(i), self.getGreen(i), self.getBlue(i))
            else:
                pix[i] = (0, 0, 0)
            
    def updateConfigDisplay(self):
        pix.fill((8, 8, 8))
    
    def updateNeoPixels(self):
        if switchIsLeft():
            self.updateConfigDisplay()
        else:
            self.updateSequenceDisplay()
        pix.show()

    def checkSwitch(self):
        # Return value indicates if NeoPixels need to be updated.
        if self.switchIsLeft != switch.value:
            self.switchIsLeft = switch.value
            return True
        else:
            return False

    # Should probably refactor these into one method

    def checkA(self):
        # Return value indicates if NeoPixels need to be updated.
        update = False
        if self.a != a_button.value:
            if a_button.value:
                self.seq.addStep()
                update = True
            self.a = a_button.value
        return update
        
    def checkB(self):
        update = False
        if self.b != b_button.value:
            if b_button.value:
                self.seq.addTrigger()
                update = True
            self.b = b_button.value
        return update

    def getByte(self):
        raw = innie.read(1)
        if raw != b'':
            # convert the byte type to a number
            return ord(raw)     
        else:
            return None
    
    def get_msg(self):
        b = self.getByte()
        return b    

    def incrementClock(self):
        self.clock_count +=1 
        if self.clock_count >= _CLOCK_LIMIT:
            self.clock_count = 0
            self.seq.incrementActiveStep()
            self.updateNeoPixels()
            led.value = not(led.value)
            
    def main(self):
        while True:
            # These method calls change state and return True or False.
            # True indicates we need to call updateNeoPixels()
            if self.checkSwitch() or self.checkA() or self.checkB():
                self.updateNeoPixels()
            msg = self.get_msg()
            if msg is not None:
                if msg == _CLOCK_MSG:
                    self.incrementClock()
