import cpx
import model

class View(object):
    '''This is the base class of all views.'''
    def __init__(self, model, pix=cpx.pix):
        self.model = model 
        self.pix = pix

    def main(self):
        self.check_buttons()
        if self.model.update_display:
            self.update_pixels()  
        return self

class PlayingView(View):
    '''This is the base class of the sequence view while the MIDI clock has started.'''
    def update_mode(self):
        # Check the switch and return current mode.
        if cpx.switch_is_left():
            self.model.update_display = True
            return ConfigView(self.model, self.pix)
        else:
            return SeqPlayingView(self.model, self.pix)

class StoppedView(View):
    '''This is the base class of the sequence view while the clock has been stopped.'''
    pass

class SeqPlayingView(PlayingView):

    def check_buttons(self):
        if cpx.a_button.went_down():
            self.model.add_step()
            self.model.update_display = True
        elif cpx.b_button.went_down():
            pass  # usually a method of the model.

    def getRed(self, i):
        if i == self.model.active_step:
            return 96
        else:
            return 0

    def getGreen(self, i):
        if self.model.sequence[i]:
            return 48
        else:
            return 0

    def getBlue(self, i):
        # add velocity calculation
        return 16

    def update_pixels(self):
        # Re-draw the neopixels.
        for i in range(self.model.led_count):
            if i < len(self.model.sequence):
                cpx.pix[i] = (self.getRed(i), self.getGreen(i), self.getBlue(i))
            else:
                cpx.pix[i] = (0, 0, 0)
        self.model.update_display = False
        cpx.pix.show()  

class SeqStoppedView(StoppedView):
    pass

class ConfigView(View):

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


