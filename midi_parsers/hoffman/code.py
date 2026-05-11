import gc
import time
import os

import adafruit_midi_parser

from adafruit_macropad import MacroPad
from adafruit_midi.note_on import NoteOn
from adafruit_midi.note_off import NoteOff





class Custom_Player(adafruit_midi_parser.MIDIPlayer):

    def on_note_on(self, note, velocity, channel):
        self.macropad.midi.send(NoteOn(note, 
                                       velocity, 
                                       channel = app_model.out_channel))
        toggle_led()

    def on_note_off(self, note, velocity, channel): 
        self.macropad.midi.send(NoteOff(note, 
                                        velocity, 
                                        channel = app_model.out_channel))
        toggle_led()

    def on_end_of_track(self, track):  
        print(f"End of track {track}")

    def on_playback_complete(self): 
        print("Playback complete, restarting...")

class AppModel():

    def __init__(self, file_names, current_file=0, selected_file=0,
                 out_channel=2, keys_changed=False):
        self.file_names = file_names
        self.current_file = current_file
        self.selected_file = selected_file
        self.out_channel = out_channel
        self.keys_changed = keys_changed

key_states = [False] * 12
macro_pad = MacroPad()
led = macro_pad.red_led
midi_player = Custom_Player()
app_model = AppModel(os.listdir('/midi'))

def toggle_led():
    led = not led

def process_key_states():
    pass


def update_keys(e):
    key_states[e.key_number] = e.pressed

def get_keys():
    key_event = macro_pad.keys.events.get()
    if key_event:
        app_model.keys_changed = True
        update_keys(key_event)
        get_keys()  # hey, recursion!

while True:
    get_keys()
    if app_model.keys_changed:
        process_key_states()
    # get_encoder()
    # if app_model.encoder_changed:
        # process_encoder_state()
    if midi_player.playing:
        midi_player.play()
    # anything else?