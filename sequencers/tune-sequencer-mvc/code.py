# SPDX-FileCopyrightText: 2025 Tom Hoffman & E-Cubed students
# SPDX-License-Identifier: MIT

# Modular Playground Simple MIDI Tune Sequencer

# Module Description:
# Sends a pre-defined sequence of MIDI notes.

import cpx

from midi_controller import Starting # type: ignore
from minimal_midi import MinimalMidi
from model import TuneModel
from board_controller import SelectorView

# send MIDI messages on:
channel_out = 1

tm = TuneModel()

mc = Starting(tm, MinimalMidi(None, channel_out))
mc.midi.clear_msgs()

bc = SelectorView(tm, mc)
bc.update_pixels()

while True:
    mc = mc.main()
    bc = bc.main()
