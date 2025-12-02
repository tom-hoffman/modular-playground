import cpx

_COLORS = ((8, 0, 16), (0, 0, 16), (0, 8, 16), (0, 16, 16), (0, 16, 8),
           (0, 16, 0), (8, 16, 0), (16, 16, 0), (16, 8, 0), (16, 0, 0))

_BASE_BRIGHTNESS = 0.2

class View(object):

    def __init__(self, model, pix=cpx.pix):
        self.model = model 
        self.pix = pix
    
    def get_mode_color(self):
        return _COLORS[self.model.tune_index]
        
    def main(self):
        self.check_buttons()
        if self.model.changed:
            self.update_pixels()  
        return self

class SelectorView(View):

    def update_pixels(self):
        c = self.get_mode_color()
        cpx.pix.brightness = _BASE_BRIGHTNESS + self.model.intensity
        cpx.pix.fill(c)
        cpx.pix[self.model.tune_index] = (32, 32, 32)
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
