# SPDX-FileCopyrightText: 2025 Tom Hoffman & E-Cubed students
# SPDX-License-Identifier: MIT

# Modular Playground Simple MIDI Sequencer

# Module Description:
# Sends a pre-defined sequence of MIDI notes.
from app import SequencePlayerApp
import gc

# listen for messages from:
channel_in = 0
# send messages on:
channel_out = 15

NOTES = (
            (# happy birthday
            ('G4', '8dn'),
            ('G4', '16n'),
         
            ('A4', '4n'),
            ('G4', '4n'),
            ('C5', '4n'),
         
            ('B4', '4n'),
            ('G4', '8dn'),
            ('G4', '16n'),
         
            ('A4', '4n'), 
            ('G4', '4n'),
            ('D5', '4n'),
         
            ('C5', '2n'),
            ('G4', '8dn'),
            ('G4', '16n'),
         
            ('G5', '4n'),
            ('E5', '4n'),
            ('C5', '4n'),
         
            ('B4', '4n'),
            ('A4', '4n'),
            ('F5', '8dn'),
            ('F5', '16n'),
         
            ('E5','4n'),
            ('C5','4n'),  
            ('D5','4n'),
            ('C5', '2n'),
            (0, '2n'),
            (0, '1n')
            ),
            (# Billie Jean riff
            ('F3', '4n'),
            ('C3', '4n'),
            ('E3', '4n'),
            ('F3', '4n'),
            ('E3', '4n'),
            ('C3', '4n'),
            ('B2', '4n'),
            ('C3', '4n')
            ),
            (# How many More Times (Led Zep.)
            ('E3', '4n'),
            ('E4', '8n'),
            ('D4', '8n'),
            ('C4', '4n'),
            ('D4', '4n'),
            ('E3', '4n'), 
            ('E4', '4n'),
            ('D4', '4n'),
            ('C4', '8n'), 
            ('D4', '8n')
            ),
            (# A Beatles riff...?
            ('E4', '8n'),
            ('E4', '8n'),
            ('D4', '16n'),
            ('E4', '16n'),
            ('G4', '8n'),
            ('E4', '4n')
            )
)


app = SequencePlayerApp(NOTES)

app.main()
gc.collect()
print("Bytes free: " + str(gc.mem_free()))
