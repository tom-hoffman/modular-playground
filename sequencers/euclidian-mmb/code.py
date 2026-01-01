# SPDX-FileCopyrightText: 2025 Tom Hoffman & E-Cubed students
# SPDX-License-Identifier: MIT

# Modular Playground Euclidian Sequencer

# Module Description:
# 

import gc

import midi_controller
print("After midi controller: " + str(gc.mem_free()))
from minimal_midi import MinimalMidi
print("After minimal_midi: " + str(gc.mem_free()))
from model import SequenceModel
print("After model: " + str(gc.mem_free()))
import board_controller

# send MIDI messages on:
# this is the "raw" 0-15 scale
channel_out = 15
# note index
note = 0
# number of notes
notes = 6
led_count = 10

tm = SequenceModel(note, notes, led_count=led_count)
tm.generate()

mc = midi_controller.Playing(tm, MinimalMidi(None, channel_out))

bc = board_controller.PlayingView(tm).update_mode()
bc.update_pixels()
print("After object creation: " + str(gc.mem_free()))

mc.midi.clear_msgs()

def update_board(m, b):
    if isinstance(m, midi_controller.Playing):
        bc = board_controller.PlayingView(bcmodel)
    else: 
        bc = board_controller.StoppedView(b.model)

while True:
    mc = mc.main()
    if tm.midi_changed:
        update_board(bc, mc)
        tm.midi_changed = False
    bc = bc.update_mode()
    bc = bc.main()
