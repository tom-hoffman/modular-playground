# Handle user and MIDI input/output
# business logic goes in model
# stay between model and view

import cpx
import midi_modes # type: ignore

from minimal_midi import MinimalMidi

from model import TuneModel  # type: ignore
from view import SelectorView # type: ignore

class TuneController(object):

    def __init__(self, model, view, midi, button_delay=0):
        self.model = model
        self.view = view
        self.midi = midi
        self.mode = midi_modes.starting
        self.button_delay = button_delay

    def update_display(self):
        self.view.update_pixels(self.model.tune_index, 
                                self.model.get_tunes_count())
        
    def check_buttons(self):
        changed = False
        cpx.a_button.update()
        cpx.b_button.update()
        if cpx.a_button.rose:
            self.model.decrement_tune()
            changed = True
        if cpx.b_button.rose:
            self.model.increment_tune()
            changed = True
        if changed:
            self.update_display()

    def main(self):
        self.check_buttons()
        msg = self.midi.get_msg()
        if msg is not None:
            self.mode = self.mode(msg)



