# SPDX-FileCopyrightText: 2025 Tom Hoffman
# SPDX-License-Identifier: MIT

# Modular Playground Binary Number Display

# Module Description:
# Displays a binary number on the CPX.

def displayByte(n, color0, color1, pix):
    # Uses bitmasks based on powers of two to display a byte
    # n is the number; color0 and color1 are RGB tuples; pix is a CPX's neopixels.
    pix[0] = OFF
    pix[9] = OFF
    for i in range(8):
        if (n & (2 ** i)):
            pix[8 - i] = color1
        else:
            pix[8 - i] = color0
    pix.show()

# set up neopixels
import neopixel
import board
import time

PURPLE = (16, 0, 16)
YELLOW = (32, 32, 0)
OFF = (0, 0, 0)

neoPixels = neopixel.NeoPixel(board.NEOPIXEL, 10, auto_write=False)
while True:
    for x in range(256):
        displayByte(x, PURPLE, YELLOW, neoPixels)
