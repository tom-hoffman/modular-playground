# SPDX-FileCopyrightText: 2025 Tom Hoffman & E-Cubed students
# SPDX-License-Identifier: MIT

# Modular Playground Simple MIDI Tune Sequencer

# Module Description:
# Sends a pre-defined sequence of MIDI notes.

import gc
print("at start: ", gc.mem_free())

from controller import Starting # type: ignore
from minimal_midi import MinimalMidi
from model import TuneModel
from view import SelectorView


# send MIDI messages on:
channel_out = 1
print("before app creation:", gc.mem_free())
app = Starting(TuneModel(),
                     SelectorView(),
                     MinimalMidi(None, channel_out))

app.midi.clear_msgs()

print("after app creation:", gc.mem_free())

while True:
    app = app.main()
