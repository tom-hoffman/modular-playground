# Circuit Playground Bit Shift CV Sequencer

# Outputs a pseudo-random stepped CV on A0,
# timed by MIDI clock.

# By Tom Hoffman.
# GPL 3.0 License.

import gc
import board
import random
import digitalio
from analogio import AnalogOut

import usb_midi
import adafruit_midi  # download from https://circuitpython.org/libraries

from adafruit_midi.timing_clock import TimingClock 

gc.collect()
print("Free bytes after imports = " + str(gc.mem_free()))

# analogio API takes a 16 bit value even though CPX has 10 bit DAC.
MAX_OUTPUT: int = (2 ** 16) - 1
analog_out = AnalogOut(board.A0)

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT
led.value = True

step_count: int = 10  # steps in sequence.
sequence: int = random.randint(0, 2 ** (step_count - 1))   # the bit register.
rungle_bits: int = 3  # bits used to calculate output.
mask_value: int = (2 ** rungle_bits) - 1

tick_count: int = 0

# utilities

def scaling(n: int, inMax: int , outMax: int) -> int:
    """Scales positive integer n from inMax range to outMax range."""
    pct: float = n / inMax
    return round(pct * outMax)

# binary utilities

def printBinary(n: int) -> None:
    print("{0:b}".format(sequence))

def getBit(n: int, bit_index: int) -> int:
    return n & (1 << bit_index)

def setBit(n: int, bit_index: int) -> int:
    return n | (1 << bit_index)

def clearBit(n: int, bit_index: int) -> int:
    return n & ~(1 << bit_index)

def shiftRight(n: int, bit_count: int) -> int:
    shifted: int = n >> 1
    if getBit(n, 0):
        return setBit(shifted, bit_count - 1)
    else:
        return clearBit(shifted, bit_count - 1)

midi = adafruit_midi.MIDI(midi_in = usb_midi.ports[0],
                          midi_out = usb_midi.ports[1])

print("Setup complete...")

gc.collect()
print("Free bytes after setups = " + str(gc.mem_free()))

while True:
    msg_in = midi.receive()
    if isinstance(msg_in, TimingClock):
        tick_count = (tick_count + 1) % 24
        if tick_count == 0:
            led.value = not(led.value)
            sequence = shiftRight(sequence, step_count)
            masked_sequence = sequence & mask_value
            output_value = scaling(masked_sequence, mask_value, MAX_OUTPUT)
            analog_out.value = output_value
