# SPDX-FileCopyrightText: 2025 Tom Hoffman & E-Cubed students
# SPDX-License-Identifier: MIT

# Modular Playground Simple MIDI Sequencer

# Module Description:
# Sends a pre-defined sequence of MIDI notes.
from app import SequencePlayerApp
from tune import NOTES

CHANNEL = 5

app = SequencePlayerApp(CHANNEL, NOTES)

app.main()

