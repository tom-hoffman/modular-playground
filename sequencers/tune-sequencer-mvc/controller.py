# Handle user and MIDI input/output
# business logic goes in model
# stay between model and view
import gc

print("controller.py before imports: ", gc.mem_free())


import cpx
gc.collect()
print("controller.py after cpx: ", gc.mem_free())


import midi_modes # type: ignore
gc.collect()
print("controller.py after midi-modes: ", gc.mem_free())


from minimal_midi import MinimalMidi
gc.collect()
print("controller.py after minimal_midi import:", gc.mem_free())


from model import TuneModel  # type: ignore

gc.collect()
print("controller.py after model import:", gc.mem_free())

from view import SelectorView # type: ignore

gc.collect()
print("controller.py after model and view imports:", gc.mem_free())


class TuneController(object):

    def __init__(self, channel_out):
        self.model = TuneModel()
        self.view = SelectorView()
        self.midi = MinimalMidi(None, channel_out)
        self.mode = midi_modes.starting

    def update_display(self):
        self.view.update_pixels(self.model.tune_index, 
                                self.model.get_tunes_count())
        
    def check_buttons(self):
        changed = False

        if cpx.a_button.went_down():
            self.model.decrement_tune()
            changed = True
        if cpx.b_button.went_down():
            self.model.increment_tune()
            changed = True
        if changed:
            self.update_display()

    def main(self):
        self.check_buttons()
        msg = self.midi.get_msg()
        if msg is not None:
            self.mode = self.mode(msg)



