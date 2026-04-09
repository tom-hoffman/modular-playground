# Handle user and MIDI input/output
# business logic goes in model
# stay between model and view

# Inputs -> NoteOn, optional CC.

import cpx
import config

class MidiController(object):

    def __init__(self, model, midi, led=cpx.led, audio=cpx.audio):
        self.model = model
        self.midi = midi
        self.led = led

    def toggle_led(self):
        self.led.value = not(self.led.value)

    def process_cc(self, msg):
        fun = msg['function']
        if fun in self.model.cc_keys:
            if config.CC_VALUES[fun] == 'sample_index':
                # change these to method calls that generate new overall counts
                self.model.sample_cc_count = msg['value']
            elif config.CC_VALUES[fun] == 'bank_index':
                self.model.bank_cc_count = msg['value']
            self.model.update_display = True

    def main(self):
        msg = self.midi.get_msg()
        if msg is not None:
            if msg['type'] == 'CC':
                self.process_cc(msg)
            elif msg['type'] == 'NoteOn':
                pass
            elif msg['type'] == 'NoteOff':
                pass
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
        
