import tune
import util

class TuneModel(object):
    def __init__(self, tune_index=0, note_index=0, clock_count=0, 
                 divider=0, pitch=0, duration=0):
        self.tune_index = tune_index
        self.note_index = note_index
        self.clock_count = clock_count
        self.divider = divider
        self.pitch = pitch
        self.duration = duration

    def get_tune(self):
        return tune.TUNES[self.tune_index]

    def get_note_pair(self):
        # Returns (pitch, duration) from the notes tuple.
        return self.getTune()[self.note_index]
    
    def set_pitch_and_duration(self):
        np = self.get_note_pair()
        self.pitch = util.note_parser(np[0])
        self.duration = util.NOTE_DURATIONS[np[1]]

    def get_tunes_count(self):
        '''Total number of tunes.'''
        return len(tune.TUNES)

    def get_tune_length(self):
        '''Length of the current tune.'''
        return len(tune.TUNES[self.tune_index])
    
    def increment_tune(self):
        self.tune_index = (self.tune_index + 1) % self.get_tunes_count()
    
    def decrement_tune(self):
        self.tune_index = (self.tune_index -1)
        if self.tune_index < 0:
            self.tune_index = self.get_tunes_count() - 1

    def stop(self):
        self.note_index = 0
        self.clock_count = 0

