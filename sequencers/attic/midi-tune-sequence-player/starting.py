from app import SequencePlayerApp
from util import *

class StartingPlayer(SequencePlayerApp):

    def process_MIDI(self):
        if self.msg['type'] == 'Clock':
            pass