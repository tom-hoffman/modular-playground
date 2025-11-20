# SPDX-FileCopyrightText: 2025 Tom Hoffman & E-Cubed students
# SPDX-License-Identifier: MIT

# Modular Playground Simple MIDI Sequencer

# Module Description:
# Sends a pre-defined sequence of MIDI notes.
from app import SequencePlayerApp
import tune

# send MIDI messages on:
channel_out = 15

app = SequencePlayerApp(tune.NOTES, channel_out)



while True:
    app.process_MIDI()
    app.updatePixels()
    app.check_buttons()


