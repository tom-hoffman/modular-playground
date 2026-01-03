import math

# CONSTANTS

MAX_VELOCITY = const(6)
DEFAULT_VELOCITY = const(4)

_CLOCK_LIMIT = const(24)  # for quarter note

def gen_mask(n, acc):
    # generates a bitmask for n bits
    if n == 1:
        return acc + 1
    else:
        return gen_mask(n - 1, acc + (2 ** (n - 1)))

class SequenceModel(object):

    def __init__(self, note_index, note_count, steps=2, triggers=1, led_count=9):
        self.note_index = note_index
        self.note_count = note_count
        self.steps = steps
        self.triggers = triggers
        self.rotation = 0
        self.sequence = [False] * steps
        self.active_step = 0
        self.velocity_index = DEFAULT_VELOCITY
        self.clock_count = 0
        self.update_display = True
        self.midi_changed = True
        self.led_count = led_count

    def generate(self):
        '''
        Generates a "Euclidian rhythm" where triggers are
        evenly distributed over a given number of steps.
        Takes in a number of triggers and steps, 
        returns a list of Booleans.
        Based on Jeff Holtzkener's Javascript implementation at
        https://medium.com/code-music-noise/euclidean-rhythms-391d879494df
        '''
        if self.triggers == 0:
            self.sequence = [False] * self.steps
        else:
            slope = self.triggers / self.steps
            result = []
            previous = None
            for i in range(self.steps):
                # adding 0.0001 to correct for imprecise math in CircuitPython.
                current = math.floor((i * slope) + 0.001) 
                result.append(current != previous)
                previous = current
            rotated = result[self.rotation:] + result[:self.rotation]
            self.sequence = rotated
            self.update_display = True

    def increment_note(self):
        self.note_index += 1

    def increment_clock(self):
        self.clock_count += 1
        if self.clock_count >= _CLOCK_LIMIT:
            self.active_step = (self.active_step + 1) % len(self.sequence)
            self.update_display = True
            self.clock_count = 0

    def is_active_step(self):
        return self.sequence[self.active_step]

    def stop_reset(self):
        self.reset_clock()
        self.active_step = 0
        self.update_display = True
        self.midi_changed = True

    def reset_clock(self):
        self.clock_count = 0

    def triggered(self):
        return 1 & self.seq

    def add_step(self):
        if self.steps < self.led_count:
            self.steps += 1
        else:
            self.steps = 1
            self.triggers = 0
            self.active_step = 0
        self.generate()

    def add_trigger(self):
        if self.triggers < self.steps:
            self.triggers += 1
        else:
            self.triggers = 0
        self.generate()
    
    def add_rotation(self):
        self.rotation = (self.rotation + 1) % self.steps
        self.generate()
    
    def sub_rotation(self):
        self.rotation -= 1
        if self.rotation < 0:
            self.rotation = self.steps - 1
        self.generate()
    
    def increment_velocity(self):
        self.velocity_index = (self.velocity_index + 1) % MAX_VELOCITY
        self.update_display = True

    def increment_note(self):
        self.note_index = (self.note_index + 1) % self.note_count
        self.update_display = True