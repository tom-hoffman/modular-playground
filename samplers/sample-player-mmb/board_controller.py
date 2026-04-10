import cpx
import config

class View(object):

    def __init__(self, model, pix=cpx.pix):
        self.model = model 
        self.pix = pix

    def main(self):
        # called by code.py regularly
        self.check_buttons()
        if self.model.update_display:
            self.update_pixels()  
        return self

class ActiveView(View):

    def update_mode(self):
        # Check the switch and return current mode.
        if cpx.switch_is_left():
            self.model.changed = True
            return ConfigurationView(self.model, self.pix)
        else:
            return self

    def check_buttons(self):
        if cpx.a_button.went_down():
            self.model.increment_bank()
        elif cpx.b_button.went_down():
            self.model.increment_sample()

    def updateBackground(self):
        self.pix.fill(config._BANK_COLORS[self.model.bank_index])

    def updateSelection(self):
        self.pix[self.sample_index] = config._SELECTION_COLOR

    def updatePixels(self):
        self.updateBackground()
        self.updateSelection()
        self.model.update_display = False
        self.pix.show()

class ConfigurationView(View):
    '''
    This view should let you change the MIDI note you're listening for.
    '''

    def check_buttons(self):
        if cpx.a_button.went_down():
            pass
        elif cpx.b_button.went_down():
            pass

    def update_mode(self):
        if cpx.switch_is_left():
            return self
        else:
            self.model.update_display = True
            return ActiveView(self.model, self.pix)    

    def update_pixels(self):
        self.pix.fill((0, 32, 0))
        self.model.update_display = False
        self.pix.show()


