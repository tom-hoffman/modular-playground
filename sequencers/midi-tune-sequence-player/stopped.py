from app import SequencePlayerApp
from starting import StartingPlayer
from util import *

class StoppedPlayer(SequencePlayerApp):

    def process_MIDI(self):
        if (self.msg['type'] == 'Start') or (self.msg['type'] == 'Continue'):
            #return Starting
            pass
        else:
            return None

            