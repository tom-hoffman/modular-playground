import cpx

class View(object):

    def __init__(self, led=cpx.led):
        self.led = led
    
    def toggle_led(self):
        self.led.value = not self.led.value

class SelectorView(View):

    def update_pixels(self, tune_index, tune_length):
        for i in range(tune_length):
            cpx.pix[i] = ((32, 0, 32))
        cpx.pix[tune_index] = (0, 32, 0)
        cpx.pix.show()
    
