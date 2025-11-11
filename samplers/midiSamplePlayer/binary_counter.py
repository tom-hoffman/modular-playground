# SPDX-FileCopyrightText: 2025 Tom Hoffman
# SPDX-License-Identifier: MIT

# Modular Playground Binary Number Display

# Module Description:
# Displays a binary number on the CPX.

from micropython import const

_OFF = const((0, 0, 0))

def displayByte(n, color0, color1, pix):
    # Uses bitmasks based on powers of two to display a byte
    # n is the number; color0 and color1 are RGB tuples; pix is a CPX's neopixels.
    pix[0] = _OFF
    pix[9] = _OFF
    for i in range(8):
        if (n & (2 ** i)):
            pix[8 - i] = color0
        else:
            pix[8 - i] = color1
    pix.show()


