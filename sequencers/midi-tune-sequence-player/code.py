# SPDX-FileCopyrightText: 2025 Tom Hoffman & E-Cubed students
# SPDX-License-Identifier: MIT

# Modular Playground Simple MIDI Sequencer

# Module Description:
# Sends a pre-defined sequence of MIDI notes.
import active
from minimal_midi import MinimalMidi
import tune
import gc

# send MIDI messages on:
channel_out = 1

app = active.ActivePlayer(tune.NOTES, MinimalMidi(None, channel_out))
app.midi.clear_msgs()
count = 0    

while True:
    got_msg = app.get_MIDI() # return boolean
    if got_msg:
        '''
        if app['msg'] == 'Stop':
            app = StoppedPlayer(self.notes,
                                self.midi.out_channel,
                                self.tuneIndex,
                                self.tune
                                0,  # reset clockCount
                                0,  # reset noteIndex
                                tune.NOTES, 
                                )
        '''
        app = app.process_MIDI()
        app.updatePixels()
    if count & 0b100000000:
        app.check_buttons()
        count = 0
        print(gc.mem_free())
        app.updatePixels()
    else:
        count += 1

'''
            return ActivePlayer(self.notes, 
                                self.midi.out_channel,
                                self.tuneIndex,
                                self.clockCount,
                                self.noteIndex,
                                self.tune,
                                self.pitch,
                                self.duration,
                                self.playing)
                                '''