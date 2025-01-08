# testing cpixUI in CircuitPython

# trying NOT to use Circuit Playground library for memory purposes

import gc
import neopixel

class Photon(object):
    NEOPIXEL_COUNT = 10
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

class HalfBar(object):
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
            self.pixels[i] = (0, 0, 0)

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

p = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=0.2, 
    auto_write=False)
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
