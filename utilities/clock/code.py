# SPDX-FileCopyrightText: 2025 Tom Hoffman & E-Cubed students
# SPDX-License-Identifier: MIT

# Modular Playground Tap Tempo Clock

# Module Description:
# This is a CircuitPython implementation of a
# tap tempo MIDI clock.
# CircuitPython is not exactly ideal for precise timing,
# so we need to make some concessions to maximize accuracy.

# If we're in Active mode, main loop just checks the timing 
# to send out a MIDI tick and occasionally the switch to 
# see if we should change modes.

# Tap mode stops the clock, because we want to be able to do that
# to reset the sequencers.

# This could be modified to keep the clock running at all times.

# In tap mode, we calculate the tempo based on the timing of 
# button taps.  For simplicity we're just doing the last two
# taps (not an average of more).


import gc
from micropython import const
import supervisor

from minimal_midi import MinimalMidi
print("After minimal_midi: " + str(gc.mem_free()))

import cpx
import config

print("After cpx and config: " + str(gc.mem_free()))

from model import ApplicationModel
print("After model: " + str(gc.mem_free()))

from board_controller import ActiveView 
print("After board controller: " + str(gc.mem_free()))

midi = MinimalMidi()

mod = ApplicationModel() 

bc = ActiveView(mod).update_mode()
cpx.led.value = False
bc.update_pixels()

def check_time():
    if cpx.ticks_less(mod.next_pulse, supervisor.ticks_ms()):
        mod.pulses += 1
        if mod.active:
            midi.send_clock()
        if mod.pulses >= config.ppqn:
            mod.pulses = 0
            mod.advance_photon()
            bc.update_pixels()
        if mod.active: 
            cpx.led.value = not(cpx.led.value)
        else:
            cpx.led.value = False
        mod.next_pulse += mod.millis_per_pulse

print("After object creation: " + str(gc.mem_free()))

mod.next_pulse = supervisor.ticks_ms() + mod.millis_per_pulse
midi.send_start()
while True:
    if mod.active: 
        for i in range(0, config.midi_repeat):
            check_time()
        bc = bc.update_mode()
        if mod.changed:
            bc.update_pixels
            mod.changed = False
        if not(mod.active):
            midi.send_stop()
    else:
        check_time()
        bc.check_buttons()
        bc = bc.update_mode()
        if mod.changed:
            bc.update_pixels
            mod.changed = False
        if mod.active:
            midi.send_start()

