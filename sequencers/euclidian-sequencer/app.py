from cpx import led, a_button, b_button, switch, switchIsLeft, pix, innie, outie

# CONSTANTS

_NOTE_COUNT = const(6)
# preset for Nord Drum 3p - 60, 62, 64, 65, 67, 69
_NOTES = const((b'\x3C', b'\x3E', b'\x40', b'\x41', b'\x43', b'\x45'))

_CLOCK_MSG = const(b'\xF8')
_LED_COUNT = const(10)
_CLOCK_LIMIT = const(24)  # for quarter note
_MAX_VELOCITY = const(5)
_DEFAULT_VELOCITY = const(4)

# todo
# MIDI start/stop/continue
# config mode
# alignment
# optimization
# skip updating display as necessary
# config file
# restart - config option?



class SequencerApp(object):
    def __init__(self, sequence):
        self.seq = sequence
        self.note_index = 0
        self.velocity_index = _DEFAULT_VELOCITY
        self.starting_step = 0
        self.clock_count = 0
        self.started = False
        self.isConfigMode = switchIsLeft()
        self.dirty = False

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
    
    def get_msg(self):
        return innie.read(1)
    
    def sendNoteOn(self):
        # 9F = ch16 note on; note60=3C; velo 64
        msg = bytes.fromhex('9F 3C 64')
        outie.write(msg)
    
    def incrementClock(self):
        self.clock_count +=1 
        if self.clock_count >= _CLOCK_LIMIT:
            self.clock_count = 0
            self.seq.incrementActiveStep()
            led.value = not(led.value)
            self.dirty = True
            if self.seq.activeStepIsTrigger():
                self.sendNoteOn() 
    
    def checkButtons(self):
        a_button.update()
        b_button.update()
        if a_button.rose:
            self.seq.addStep()
            self.dirty = True
        elif b_button.rose:
            self.seq.addTrigger()
            self.dirty = True

    
    def main(self):
        delay_count = 0
        while True:
            delay_count += 1
            if delay_count == 127:
                delay_count = 0
                self.checkButtons()
            msg = self.get_msg()
            if msg == _CLOCK_MSG:
                self.incrementClock()
            if self.dirty:
                self.updateNeoPixels()
                self.dirty = False

