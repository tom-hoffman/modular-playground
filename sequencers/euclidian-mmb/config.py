# config.py

# Put starting variables here that might need to be changed by the user.

# Give each Circuit Playground a unique name so you don't get confused!
USB_NAME = "EUCLID0"

# send MIDI messages on:
# this is the "raw" 0-15 scale
channel_out = 15

# These are the note values each sequencer will put out.
# preset for Nord Drum 3p - 60, 62, 64, 65, 67, 69
NOTE_NUMBERS = (60, 62, 64, 65, 67, 69)

# The note index THIS sequence sends out:
note = 0

# pulses per quarter note
PPQN = 24

# starting values for the sequencer
DEFAULT_VELOCITY = 4
DEFAULT_STEPS = 4
DEFAULT_TRIGGERS = 1
DEFAULT_ROTATION = 0


