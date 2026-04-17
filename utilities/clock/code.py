# SPDX-FileCopyrightText: 2025 Tom Hoffman & E-Cubed students
# SPDX-License-Identifier: MIT

# Modular Playground Application Template

# Module Description:
# 

import gc

from minimal_midi import MinimalMidi
print("After minimal_midi: " + str(gc.mem_free()))
from model import ApplicationModel
print("After model: " + str(gc.mem_free()))

from board_controller import ActiveView



tm = ApplicationModel()

mc = Starting(tm, MinimalMidi(None, channel_out))
mc.midi.clear_msgs()

bc = ActiveView(tm).update_mode()
bc.update_pixels()
print("After object creation: " + str(gc.mem_free()))
while True:
    mc = mc.main()
    bc = bc.update_mode()
    bc = bc.main()
