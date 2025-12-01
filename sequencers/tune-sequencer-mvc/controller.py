# Handle user and MIDI input/output
# business logic goes in model
# stay between model and view

import cpx

class TuneController(object):

    def __init__(self, model, view, midi):
        self.model = model
        self.view = view
        self.midi = midi
        
    def check_buttons(self):
        changed = False
        if cpx.a_button.went_down():
            self.model.decrement_tune()
            changed = True
        if cpx.b_button.went_down():
            self.model.increment_tune()
            changed = True
        if changed:
            self.view.update_pixels(self.model.tune_index, 'button')

    def main(self):
        self.check_buttons()
        msg = self.midi.get_msg()
        if msg is not None:
            self.view.toggle_led()
            if msg['type'] == 'Clock':
                return self.next()
            elif msg['type'] == 'Stop':
                self.model.reset_tune()
                self.view.update_pixels(self.model.tune_index, 'stopped')
                return Stopped(self.model, self.view, self.midi)
            elif msg['type'] == 'Start':
                return Starting(self.model, self.view, self.midi)
            else:
                return self
        else:
            return self

class Starting(TuneController):

    def next(self):
        self.model.advance_pitch_and_duration()
        if self.model.pitch:
            self.midi.send_note_on(self.model.pitch, 127)
        else:
            self.midi.send_note_off(0)
        self.view.update_pixels(self.model.tune_index, 'starting')
        return Sustaining(self.model, self.view, self.midi)

class Sustaining(TuneController):

    def next(self):
        self.model.clock_count += 1
        self.midi.send_note_off(self.model.pitch)
        self.view.update_pixels(self.model.tune_index, 'sustaining')
        return Counting(self.model, self.view, self.midi)

class Counting(TuneController):

    def next(self):
        if self.model.clock_count == 1:
            self.view.update_pixels(self.model.tune_index, 'counting')
        self.model.clock_count += 1
        if self.model.clock_count >= (self.model.duration - 1):
            return Starting(self.model, self.view, self.midi)
        else:
            return self

class Stopped(TuneController):
    def next(self):
        return self
        
