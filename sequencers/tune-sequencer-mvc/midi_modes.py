
class MidiMode(object):

    def __init__(self, midi):
        self.midi = midi
    
    def get_midi(self):
        return self.midi.get_msg()

class Starting(MidiMode):
    '''Waiting to play a note the next clock.'''
    def next(self, msg):
        if msg['type'] == 'Clock':
            msg
            return Starting(self.midi) # not starting!

class Sustaining(MidiMode):
    '''Currently only sustining 1 clock cycle.  Could be adjustible'''
    def next(self, msg):
        return
'''
def starting(msg):
    if msg['type'] == 'clock':

    return starting

def stopped(msg):
    pass

def counting(msg):
    pass

def sustaining(msg):
    pass

'''