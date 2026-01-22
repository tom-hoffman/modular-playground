import cpx
import model
from config import *

_BASE_BRIGHTNESS = 0.2
_BACKGROUND = (16, 0, 16)
_CURSOR = (32, 32, 0)

class View(object):

    def __init__(self, model, pix=cpx.pix):
        self.model = model 
        self.pix = pix
        
    def main(self):
        self.check_buttons()
        if self.model.changed:
            self.update_pixels()  
        return self
    


class SelectorView(View):

    def update_mode(self):
        if cpx.switch_is_left():
            self.model.changed = True
            return DividerView(self.model, self.pix)
        else:
            return self

    def update_pixels(self):
        cpx.pix.brightness = _BASE_BRIGHTNESS + self.model.intensity
        cpx.pix.fill(_BACKGROUND)
        cpx.pix[self.model.tune_index] = _CURSOR
        self.model.changed = False
        cpx.pix.show()

    def check_buttons(self):
        if cpx.a_button.went_down():
            self.model.decrement_tune()
        elif cpx.b_button.went_down():
            self.model.increment_tune()

class DividerView(View):

    def check_buttons(self):
        if cpx.a_button.went_down():
            self.increment_rate()
        elif cpx.b_button.went_down():
            pass

    def update_mode(self):
        if cpx.switch_is_left():
            return self
        else:
            self.model.changed = True
            return SelectorView(self.model, self.pix)    

    def update_pixels(self):
        self.pix.fill((0, 0, 0))
        self.pix[self.model.divider_index] = (0, 16, 0)
        self.model.changed = False
        self.pix.show()

    def increment_rate(self):
        self.model.divider_index = (self.model.divider_index - 1) % len(model.DIVIDERS)
        self.model.changed = True

