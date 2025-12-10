import cpx
import model

class View(object):

    def __init__(self, model, pix=cpx.pix):
        self.model = model 
        self.pix = pix

    def main(self):
        # called by code.py regularly
        self.check_buttons()
        if self.model.changed:
            self.update_pixels()  
        return self

class ActiveView(View):

    def update_pixels(self):
        # Re-draw the neopixels.
        cpx.pix.show()

    def update_mode(self):
        if cpx.switch_is_left():
            self.model.changed = True
            return ConfigurationView(self.model, self.pix)
        else:
            return self
    
    def check_buttons(self):
        if cpx.a_button.went_down():
            pass  # usually a method of the model.
        elif cpx.b_button.went_down():
            pass  # usually a method of the model.

class ConfigurationView(View):

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

