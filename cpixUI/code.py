# testing cpixUI in CircuitPython

# trying NOT to use Circuit Playground library for memory purposes

import gc
import board
import neopixel


lStart = 4
rStart = 5

class HalfBar(object):
    # HalfBar :: (pixels :: list<tuple><int>, 
    #             length :: int, color :: tuple<int>) -> HalfBar
    def __init__(self, pixels, length, color):
        self.pixels = pixels
        if length > 5:
            self.length = 5
        elif length < 0:
            length = 0
        else:
            self.length = length
        self.color = color

class LeftBar(HalfBar):
    # this starts at pixel 4 and goes clockwise to pixel 0
    def clear(self):
        for i in range(0, lStart + 1):
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
        for i in range(rStart, 10):
            self.pixels[i] = (0, 0, 0)

    def draw(self):
        self.clear()
        end = rStart + self.length
        for i in range(rStart, end):
            self.pixels[i] = self.color
        self.pixels.show()

p = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=0.2, auto_write=False)
l = LeftBar(p, 3, (32, 0, 0))
l.draw()
r = RightBar(p, 3, (0, 32, 0))
r.draw()
print(gc.mem_free())
while 1:
    pass