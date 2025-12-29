# Handle user and MIDI input/output
# business logic goes in model
# stay between model and view

import cpx

class MidiController(object):

    def __init__(self, model, midi, led=cpx.led):
        self.model = model
        self.midi = midi
        self.led = led

    def toggle_led(self):
        self.led.value = not(self.led.value)

    def main(self):
        msg = self.midi.get_msg()
        if msg is not None:
            # process msg
            return self
        else:
            return self

class Starting(MidiController):

    def next(self):
        '''This is a sub-class of MidiController representing a state of the midi parser.
        It implements next() which returns the next state of the parser.
        e.g., from Starting to Sustaining (a note).'''
        return self

class Stopped(MidiController):
    def next(self):
        return self
        
