import cpx
import supervisor

class View(object):

    def __init__(self, model, pix=cpx.pix):
        self.model = model 
        self.pix = pix

class ActiveView(View):

    def update_mode(self):
        # Check the switch and return current mode.
        if cpx.switch_is_left():
            self.model.active = False
            self.model.last_tap = None
            self.update_pixels()
            return TapView(self.model, self.pix)
        else:
            return self

    def check_buttons(self):
        pass
    
    def update_pixels(self):
        # Re-draw the neopixels.
        self.pix.fill((0, 8, 0))
        self.pix[self.model.photon] = (32, 32, 32)
        cpx.pix.show()

class TapView(View):

    def check_buttons(self):
        if cpx.a_button.went_down() or cpx.b_button.went_down():
            if self.model.last_tap:
                new = supervisor.ticks_ms()
                self.model.update_millis(new)

            else:
                self.model.last_tap = supervisor.ticks_ms()


    def update_mode(self):
        if cpx.switch_is_left():
            return self
        else:
            self.model.active = True
            self.model.changed = True
            return ActiveView(self.model, self.pix)    

    def update_pixels(self):
        self.pix.fill((8, 0, 0))
        self.pix[self.model.photon] = (32, 32, 32)
        cpx.pix.show()


