import gc
gc.collect()
gc.mem_free()
print("model.py before imports:", gc.mem_free())

import tune
gc.collect()
gc.mem_free()
print("model.py after tune import:", gc.mem_free())



import util
gc.collect()
gc.mem_free()
print("model.py after util import:", gc.mem_free())


class TuneModel(object):
    def __init__(self, tune_index=0, note_index=0, clock_count=0, 
                 divider=0, pitch=0, duration=0):
        self.tune_index = tune_index
        self.note_index = note_index
        self.clock_count = clock_count
        self.divider = divider
        self.pitch = pitch
        self.duration = duration
    
    def set_pitch_and_duration(self):
        np = tune.TUNES[self.tune_index][self.note_index]
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

