# Handle user and MIDI input/output
# business logic goes in model
# stay between model and view

from micropython import const
import cpx

_NOTE_COUNT = const(6)
# preset for Nord Drum 3p - 60, 62, 64, 65, 67, 69
_NOTES = (60, 62, 64, 65, 67, 69)

_VELOCITY_COUNT = const(6)
_VELOCITIES = const((0, 25, 50, 75, 100, 127))

class MidiController(object):

    def __init__(self, model, midi, led=cpx.led):
        self.model = model
        self.midi = midi
        self.led = led

    def main(self):
        msg = self.midi.get_msg()
        if msg is not None:
            if msg['type'] == 'Clock':
                return self.clock()
            if msg['type'] == 'Start':
                self.model.midi_changed = True
                return Playing(self.model, self.midi)
            elif msg['type'] == 'Stop':
                self.model.midi_changed = True
                self.model.stop_reset()
                return Stopped(self.model, self.midi)
            else:
                return self
        else:
            return self

class Playing(MidiController):        
    def clock(self):
        if self.model.clock_count == 0:
            self.led.value = not self.led.value
            if self.model.is_active_step():
                self.midi.send_note_on(_NOTES[self.model.note_index],
                                       _VELOCITIES[self.model.velocity_index])
        self.model.increment_clock()
        return self

class Stopped(MidiController):
    def clock(self):
        return self

