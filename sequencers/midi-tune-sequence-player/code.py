# SPDX-FileCopyrightText: 2025 Tom Hoffman & E-Cubed students
# SPDX-License-Identifier: MIT

# Modular Playground Simple MIDI Sequencer

# Module Description:
# Sends a pre-defined sequence of MIDI notes.
import active
import tune
import gc

# send MIDI messages on:
channel_out = 1

app = active.ActivePlayer(tune.NOTES, channel_out)

count = 0

while True:
    app = app.get_MIDI()
    app.updatePixels()
    app.check_buttons()
    if count & 0b100000000:
        count = 0
        print(gc.mem_free())
    else:
        count += 1


