import cpx
from midi_controller import *

_RED = (8, 0, 0)
_GREEN = (0, 255, 0)
_BLUE = (0, 0, 255)
_CYAN = (0, 16, 16)
_PURPLE = (6, 0, 6)
_YELLOW = (64, 64, 0)
_WHITE = (32, 32, 32)
_ORANGE = (32, 16, 0)
_BLACK = (0, 0, 0)
_OFF = _BLACK

class View(object):

    def __init__(self, model, midi_controller, pix=cpx.pix):
        self.model = model 
        self.midi_controller = midi_controller
        self.pix = pix
    
    def get_mode_color(self):
        if isinstance(self.midi_controller, Counting):
            return _PURPLE
        elif isinstance(self.midi_controller, Sustaining):
            return _YELLOW
        elif isinstance(self.midi_controller, Starting):
            return _CYAN
        elif isinstance(self.midi_controller, Stopped):
            return _RED
        else:
            return _ORANGE
        
    def main(self):
        self.check_buttons()
        return self

class SelectorView(View):

    def update_pixels(self):
        c = self.get_mode_color()
        cpx.pix.fill(c)
        cpx.pix[self.model.tune_index] = _WHITE
        self.model.changed = False
        cpx.pix.show()

    def check_buttons(self):
        changed = False
        if cpx.a_button.went_down():
            self.model.decrement_tune()
            self.model.changed = True
        if cpx.b_button.went_down():
            self.model.increment_tune()
            self.model.changed = True
        if self.model.changed:
            self.update_pixels()   
