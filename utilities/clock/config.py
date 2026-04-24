# config.py

# Put starting variables here that might need to be changed by the user.

# Give each Circuit Playground a unique name so you don't get confused!
# Note that a MIDI network should only have one clock 
# so you don't need to add an identifying number
USB_NAME = "CLOCK"

# Starting value for time between MIDI clock pulses 
# the official default is 24 per quarter note
# but this is often increased by doubling
# 28 milliseconds per pulse equates to 90 bpm (arguably)
millis_per_pulse: int = 28

# Pulses per quarter note
ppqn = 24

# Number of times we check the clock and potentially send a
# message between board updates (in ActiveView)
midi_repeat: int = 256



