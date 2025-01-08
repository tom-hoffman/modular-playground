# testing cpixUI in CircuitPython

# trying NOT to use Circuit Playground library for memory purposes

import gc
import board
import neopixel

lStart = 4
lEnd   = 0
rStart = 5
rEnd   = 9

class HalfBar(object):
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
        for i in range(lEnd, lStart + 1):
            self.pixels[i] = (0, 0, 0)

    def draw(self):
        self.clear()
        end = lStart - self.length + 1
        for i in range(end, lStart + 1):
            self.pixels[i] = self.color
        self.pixels.show()

class RightBar(HalfBar):
    # this starts at pixel 5 and goes anticlockwise to pixel 9
    def clear(self):
        for i in range(rStart, rEnd + 1):
            self.pixels[i] = (0, 0, 0)
    def draw(self):
        self.clear()
        end = rStart + self.length
        for i in range(rStart, end):
            self.pixels[i] = self.color
        self.pixels.show()

p = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=0.2, 
    auto_write=False)
l = LeftBar(p, 3, (32, 0, 0))
l.add()
l.draw()
r = RightBar(p, 0, (0, 32, 0))
r.subtract()
r.subtract()
r.draw()
print(gc.mem_free())
while 1:
    pass
