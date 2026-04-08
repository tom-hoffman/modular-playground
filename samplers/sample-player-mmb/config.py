# config.py

# Put starting variables here that might need to be changed by the user.

# Assign this CPX a unique integer identifier (1 - 9) for its type in your system.
CPX_NUMBER = 0

# Give each Circuit Playground a unique name so you don't get confused!
USB_NAME = "PLAYER" + str(CPX_NUMBER)


BANKS = ("kick", "snare", "perc")

_BANK_COLORS = ((0, 0, 16), (16, 0, 0), (0, 16, 0))
_SELECTION_COLOR = (16, 16, 16)

# Listen for MIDI messages on:
# this is the "raw" 0-15 scale
channel_in = 15

# MIDI repeat count
# this is the number of times we check and process the MIDI queue 
# for every time we check and update the board buttons, neopixels, etc.
# raise this value if you are getting audible rhythm lag
# which will in turn increase button and neopixel lag
MIDI_READ_REPEAT = 256

# This is the note values each sequencer will listen for.
note_number = 60

# CC values
# Leave this empty if you don't want/need CC control
CC_VALUES = (16) 

# temporary MIDI notes ;-)

# CC messages are 1011 + channel nybble
# 0 + 7 bit controller number
# 0 + 7 bit value

# MPK knob notes...
# start at lowest value, go up to highest 7F by default.
# so we can just add this to the current number?
# we do need to store it in the model.

