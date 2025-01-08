# cpixUI: a user interface library for the Modular Playground project.
# The widgets should also be generally useful for 
# Adafruit Circuit Playground applications.

# copyright: Tom Hoffman, 2025.
# license: GPL v3.0

# Widgets:
# Flasher: a tuple of neopixels toggling on and off.
# Photon: a single neopixel which can be moved around the neopixels.
# WholeBar: an anticlockwise bar graph starting at neopixel 0.
# HalfBar: base class for 0-5 bar graphs.

import gc
import neopixel

class CPixUI(object):
    """Base class for widgets, mostly shared constants."""
    # Possibly useless.
    NEOPIXEL_COUNT = 10
    NO_LIGHT = (0, 0, 0)
    DIM_WHITE = (32, 32, 32)

# Flasher :: (pixels :: list<tuple><int>, lit :: bool, 
#             color :: tuple<int>) -> Flasher
class Flasher(CPixUI):
    """Toggles pixels on/off."""
    def __init__(self, pixels, lit = False, color = (32, 32, 32)):
        self.pixels = pixels
        self.lit = lit
        self.color = color
    def draw(self):
        print(self.lit)
        if self.lit:
            c = self.color
        else:
            c = self.NO_LIGHT
        for i in range(0, len(self.pixels)):
            self.pixels[i] = c
        self.pixels.show()
    def toggle(self):
        self.lit = not self.lit
        self.draw()
                
class Photon(CPixUI):
    # Photon :: (pixels :: list<tuple><int>, 
    #            position :: int, color :: tuple<int>) -> Photon
    def __init__(self, pixels, position, color):
        self.pixels = pixels
        self.position = position % self.NEOPIXEL_COUNT
        self.color = color
    
    def draw(self):
        self.pixels[self.position] = self.color
        self.pixels.show()

    def advanceClockwise(self):
        self.position = (self.position - 1) % self.NEOPIXEL_COUNT
    
    def advanceAntiClockwise(self):
        self.position = (self.position + 1) % self.NEOPIXEL_COUNT

class Selector(CPixUI):
    """A clockwise selector, starting at neopixel 9 (right of USB),
    with a Photon indicator."""
    # Selector :: (pixels :: list<tuple><int>, )    

class HalfBar(CPixUI):
    LEFT_START  = 4
    LEFT_END    = 0
    RIGHT_START = 5
    RIGHT_END   = 9
    # HalfBar :: (pixels :: list<tuple><int>, 
    #             length :: int, color :: tuple<int>) -> HalfBar
    def __init__(self, pixels, length, color):
        self.pixels = pixels
        self.length = length % 6
        self.color = color
        
    def add(self):
        self.length = (self.length + 1) % 6

    def subtract(self):
        self.length = (self.length - 1) % 6

class LeftBar(HalfBar):
    # this starts at pixel 4 and goes clockwise to pixel 0
    def clear(self):
        for i in range(self.LEFT_END, self.LEFT_START + 1):
            self.pixels[i] = self.NO_LIGHT

    def draw(self):
        self.clear()
        end = self.LEFT_START - self.length + 1
        for i in range(end, self.LEFT_START + 1):
            self.pixels[i] = self.color
        self.pixels.show()

class RightBar(HalfBar):
    # this starts at pixel 5 and goes anticlockwise to pixel 9
    def clear(self):
        for i in range(self.RIGHT_START, self.RIGHT_END + 1):
            self.pixels[i] = (0, 0, 0)
    def draw(self):
        self.clear()
        end = self.RIGHT_START + self.length
        for i in range(self.RIGHT_START, end):
            self.pixels[i] = self.color
        self.pixels.show()


import board
import time
p = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=0.2, auto_write=False)
fl = Flasher(p)
fl.toggle()
time.sleep(1)
fl.toggle()
time.sleep(1)
l = LeftBar(p, 3, (32, 0, 0))
l.add()
l.draw()
r = RightBar(p, 0, (0, 32, 0))
r.subtract()
r.subtract()
r.draw()
pho = Photon(p, 0, (128, 128, 128))
pho.advanceClockwise()
pho.draw()


print(gc.mem_free())

while 1:
    pass
