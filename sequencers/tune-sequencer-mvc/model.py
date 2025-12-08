
import os

TUNE_COUNT = 10
DIVIDERS = [3, 2, 1, 0.5, (1/3)]

_NOTE_DURATIONS = {'32n' : 3,
                  '16n' : 6,
                  '8n' : 12,
                  '4n' : 24,
                  '2n' : 48,
                  '1n' : 96,
                  '1dn' : 144,
                  '2dn' : 72,
                  '4dn' : 36,
                  '8dn' : 18}

def note_parser(midstr):
    if midstr == "REST":
        return 0
    Notes = (("C"),("C#","Db"),("D"),("D#","Eb"),("E"),("F"),("F#","Gb"),("G"),("G#","Ab"),("A"),("A#","Bb"),("B"))
    answer = 0
    i = 0
    letter = midstr[:-1]
    for note in Notes:
        for form in note:
            if letter.upper() == form:
                answer = i
                break
        i += 1
    #Octave
    answer += (int(midstr[-1]))*12  
    return answer

def read_lines_generator(filepath):
    '''This is a special type of function called a generator.
    It returns a single line of the tune and "pauses" at the yield statement.
    This means we don't have to load the entire song file at once,
    saving memory (at the price of apparently no significant speed).'''
    with open(filepath, 'r') as f:
        for line in f:
            yield line.strip()

def open_file(tune_index):
    '''Returns a generator for reading tunes line by line.'''
    path = str(tune_index) + '/'
    file_name = os.listdir(path)[0]
    full_path = path + file_name
    return read_lines_generator(full_path)
    
class TuneModel(object):
    def __init__(self, tune_index=0, clock_count=0, 
                 divider_index=2, pitch=0, duration=0,
                 intensity=3, changed=True):
        self.tune_index = tune_index
        self.clock_count = clock_count
        self.divider_index = divider_index
        self.pitch = pitch
        self.duration = duration
        self.tune_generator = open_file(self.tune_index)
        self.intensity = intensity
        self.changed = changed

    def reset_tune(self):
        self.clock_count = 0
        self.tune_generator = open_file(self.tune_index)

    def get_next_line(self):
        try:
            return next(self.tune_generator)
        except StopIteration:
            # start over if we've gotten to the end of the file
            # and call this function again
            self.tune_generator = open_file(self.tune_index)
            return self.get_next_line()

    def advance_pitch_and_duration(self):
        '''Get the pitch and duration of the next note.  Reset clock_count.'''
        line = self.get_next_line()
        self.clock_count = 0
        pair = line.split(',')
        raw_pitch = pair[0]
        if not raw_pitch:  # if it is a blank line
            self.advance_pitch_and_duration()
        else:
            self.duration = _NOTE_DURATIONS[pair[1].strip()] // DIVIDERS[self.divider_index]
            self.pitch = note_parser(raw_pitch.strip())

    def update_tune(self):
        self.tune_generator.close()
        self.tune_generator = open_file(self.tune_index)
        self.reset_tune()

    def increment_tune(self):
        self.tune_index = (self.tune_index + 1) % TUNE_COUNT
        self.update_tune()

    def decrement_tune(self):
        self.tune_index = (self.tune_index -1)
        if self.tune_index < 0:
            self.tune_index = TUNE_COUNT - 1
        self.update_tune()

    def increment_tune(self):
        self.tune_index = (self.tune_index + 1) % TUNE_COUNT
        self.update_tune()
        self.changed = True

    def decrement_tune(self):
        self.tune_index = (self.tune_index -1)
        if self.tune_index < 0:
            self.tune_index = TUNE_COUNT - 1
        self.update_tune()
        self.changed = True

