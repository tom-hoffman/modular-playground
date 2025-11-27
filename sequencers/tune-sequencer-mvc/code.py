# SPDX-FileCopyrightText: 2025 Tom Hoffman & E-Cubed students
# SPDX-License-Identifier: MIT

# Modular Playground Simple MIDI Tune Sequencer

# Module Description:
# Sends a pre-defined sequence of MIDI notes.

import gc
print("at start: ", gc.mem_free())

from controller import TuneController # type: ignore


# send MIDI messages on:
channel_out = 1
gc.collect()
print("before app creation:", gc.mem_free())
app = TuneController(channel_out)

app.update_display()
app.midi.clear_msgs()
print("after app creation:", gc.mem_free())
while True:
    app.main()
