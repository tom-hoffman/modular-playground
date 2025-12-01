# Handle user and MIDI input/output
# business logic goes in model
# stay between model and view

import cpx

class MidiController(object):

    def __init__(self, model, midi, led=cpx.led):
        self.model = model
        self.midi = midi
        self.led = led

    def toggle_led(self):
        self.led.value = not(self.led.value)

    def main(self):
        msg = self.midi.get_msg()
        if msg is not None:
            self.toggle_led()
            if msg['type'] == 'Clock':
                return self.next()
            elif msg['type'] == 'Stop':
                self.model.reset_tune()
                self.model.changed = True
                return Stopped(self.model, self.midi)
            elif msg['type'] == 'Start':
                self.model.changed = True
                return Starting(self.model, self.midi)
            else:
                return self
        else:
            return self

class Starting(MidiController):

    def next(self):
        self.model.advance_pitch_and_duration()
        if self.model.pitch:
            self.midi.send_note_on(self.model.pitch, 127)
        else:
            self.midi.send_note_off(0)
        self.model.changed = True
        return Sustaining(self.model, self.midi)

class Sustaining(MidiController):

    def next(self):
        self.model.clock_count += 1
        self.midi.send_note_off(self.model.pitch)
        self.model.changed = True
        return Counting(self.model, self.midi)

class Counting(MidiController):

    def next(self):
        if self.model.clock_count == 1:
            self.model.changed = True
        self.model.clock_count += 1
        if self.model.clock_count >= (self.model.duration - 1):
            self.model.changed = True
            return Starting(self.model, self.midi)
        else:
            return self

class Stopped(MidiController):
    def next(self):
        return self
        
