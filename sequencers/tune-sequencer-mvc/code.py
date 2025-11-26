# SPDX-FileCopyrightText: 2025 Tom Hoffman & E-Cubed students
# SPDX-License-Identifier: MIT

# Modular Playground Simple MIDI Tune Sequencer

# Module Description:
# Sends a pre-defined sequence of MIDI notes.

from controller import TuneController # type: ignore
from model import TuneModel # type: ignore
from view import SelectorView # type: ignore
from minimal_midi import MinimalMidi


import gc

# send MIDI messages on:
channel_out = 1


app = TuneController(TuneModel(),
                    SelectorView(),
                    MinimalMidi(None, channel_out))

app.update_display()
app.midi.clear_msgs()

while True:
    app.main()