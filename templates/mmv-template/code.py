# SPDX-FileCopyrightText: 2025 Tom Hoffman & E-Cubed students
# SPDX-License-Identifier: MIT

# Modular Playground Application Template

# Module Description:
# 

import gc

from midi_controller import Starting 
print("After midi controller: " + str(gc.mem_free()))
from minimal_midi import MinimalMidi
print("After minimal_midi: " + str(gc.mem_free()))
from model import ApplicationModel
print("After model: " + str(gc.mem_free()))

from board_controller import ActiveView

# send MIDI messages on:
channel_out = 1

tm = TuneModel()

mc = Starting(tm, MinimalMidi(None, channel_out))
mc.midi.clear_msgs()

bc = SelectorView(tm)
bc.update_pixels()
print("After object creation: " + str(gc.mem_free()))
while True:
    mc = mc.main()
    bc = bc.main()
