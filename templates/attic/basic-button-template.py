# SPDX-FileCopyrightText: 2025 Tom Hoffman
# SPDX-License-Identifier: MIT

# Modular Playground Basic Button Application Template

# Module Description:
# Starting example/template for button and switch interaction

# Put gc.mem_free() checks and other print statements inside
# conditionals which will only run when DEV_MODE is True.
# Code will run faster with DEV_MODE set to False.
# Before release, you can delete those code blocks for better performance.
DEV_MODE = True

# We use the gc library to check and manage available RAM during development
if DEV_MODE:
    import gc
    gc.collect()
    print("Starting free bytes (after gc) = " + str(gc.mem_free()))

import board            # helps set up pins, etc. on the board
import digitalio        # digital (on/off) output to pins, including board LED.
import neopixel         # controls the RGB LEDs on the board

if DEV_MODE:
    gc.collect()
    print("Free bytes after imports = " + str(gc.mem_free()))

############

# CONSTANTS
# Use ALL_CAPS_WITH_UNDERSCORE for named values that do not change.

# COLORS
# Delete the ones you don't need.
# Add others as needed!

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
PURPLE = (255, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
OFF = BLACK

############

# variables
# use lower case with underscores for variables
# delete ones you don't need and add others

# this is the active selection (song, sound, etc.)
selection = 0

############

# board setup steps

# set up the red LED
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT
led.value = True

# set up A button w/helper function
a_button = digitalio.DigitalInOut(board.BUTTON_A)
a_button.direction = digitalio.Direction.INPUT
a_button.pull = digitalio.Pull.DOWN

def aIsDown():
    return a_button.value

# set up B button w/helper function
b_button = digitalio.DigitalInOut(board.BUTTON_B)
b_button.direction = digitalio.Direction.INPUT
b_button.pull = digitalio.Pull.DOWN

def bIsDown():
    return b_button.value

# set up switch with helper function
switch = digitalio.DigitalInOut(board.SLIDE_SWITCH)
switch.direction = digitalio.Direction.INPUT
switch.pull = digitalio.Pull.UP

def switchIsLeft():
    return switch.value

# set up neopixels
neoPixels = neopixel.NeoPixel(board.NEOPIXEL, 10)

if DEV_MODE:
    gc.collect()
    print("Free bytes after setup = " + str(gc.mem_free()))

############

# functionDefinitions
# Use camelCase for function definitions:
# First letter lower case, first letter of new words upper case.


############
# Main loop(s)

while True:
    print((aIsDown(), bIsDown(), switchIsLeft()))
