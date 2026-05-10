from adafruit_macropad import MacroPad
from adafruit_hid.keycode import Keycode
import board
import digitalio
import gc
import time
import adafruit_midi_parser
import os
import usb_midi
import adafruit_midi
from adafruit_midi.note_on import NoteOn
from adafruit_midi.note_off import NoteOff

import keypad

import Input



### Main app class // Add note player // Midi Channel Selector (Keys)
# ignore the terrible code ToT
# midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], out_channel=9)

class input(Input.inputHandler):
    def __init__(self, macroPad):
        super().__init__(macroPad)

# Create a custom player class
class Custom_Player(adafruit_midi_parser.MIDIPlayer):
    def __init__(self, midi_parser, macroPad):
        super().__init__(midi_parser)
        self.macropad = macroPad
        self.send_channel = 4
        

    # def update(self, channel=None):
    #     self.macropad.out_channel=channel

    def on_note_on(self, note, velocity, channel):  # noqa: PLR6301
        # print(f"Note On: {note}, velocity: {velocity}")
        self.macropad.midi.out_channel = self.send_channel
        #print(f"Playing note {note} with velocity {velocity} on channel {self.send_channel}")
        self.macropad.midi.send(NoteOn(note, 120, channel=self.send_channel)) # Play middle C
        #led.value = True

    def on_note_off(self, note, velocity, channel):  # noqa: PLR6301
        #print(f"Note Off: {note}")
        self.macropad.midi.out_channel = self.send_channel
        self.macropad.midi.send(NoteOff(note, 120, channel=self.send_channel)) # Stop the note
        #led.value = False

    def on_end_of_track(self, track):  # noqa: PLR6301
        print(f"End of track {track}")

    def on_playback_complete(self):  # noqa: PLR6301
        print("Playback complete, restarting...")
        
class app():
    def __init__(self):
        print("Initializing app...")
        os.chdir('/midi')
        self.filesystem = os.listdir("/midi")
        self.curFile = 0
        self.selectedFile = 0
        self.fileAmt = len(self.filesystem)
        self.filename = self.filesystem[self.curFile]

        # Display
        self.macropad = MacroPad()
        self.text_lines = self.macropad.display_text(title="MacroPad Info")

        # Metadata
        self.title = 'song title'
        self.filename = 'Untitled.mid'

        self.filesystem = os.listdir("/midi/")

        self.curfile = 0
        self.fileAmt = len(self.filesystem)

        self.c1 = 0
        self.c2 = 0
        self.cSel = 0 #CSELLLLLLLL, CSELLL I NEED YOU CSELL (it selects betweem c1 and c2 T^T')

        #self.input = Input.inputHandler()
        self.input = input(self.macropad)

        self.input.__init__(self.macropad)

        self.keysDown = [False] * 12

        # Input Settings
        
        self.input.encoder_maxValue = self.fileAmt - 1
        self.input.sensitivity = 2
        self.key_event = self.macropad.keys.events.get()


        self.elapsed = 0

        self.midi_parser = adafruit_midi_parser.MIDIParser()
    
        self.midi_parser.clear()
        gc.collect()
        #print("free memory: " + str(gc.mem_free()))
        self.channel = 2 # doesnt do anything yet
        self.midi_parser.parse(self.filename)
        self.noteCount = self.midi_parser.note_count
        self.bpm = self.midi_parser.bpm

        self.playing = False
        self.playback_position = 0

        self.player = Custom_Player(self.midi_parser, self.macropad)

        self.typeMode = True
        #self.midi_parser.set_player(self.player)

    def checkMaxFiles(self):
        if self.curFile >= (self.fileAmt - 1):
            print(self.curFile)
            self.curFile = 0   
            print("Resetting to first file.")

    def setChannel(self, channel):
        if channel < 17 and channel > 0:
            self.channel = channel
            self.player.send_channel = channel
            print("Set MIDI output channel to: " + str(channel))
        else:
            print("Invalid channel number: " + str(channel) + " // Channel must be between 1 and 16.")
            
    def loadFile(self, filename):
        
        gc.collect()
        #print("free memory: " + str(gc.mem_free()))
        try:
            if (filename.endswith('.mid') or filename.endswith('.midi')) and (filename in self.filesystem):
                self.midi_parser.clear()
                self.midi_parser.parse(filename)
                self.noteCount = self.midi_parser.note_count
                self.bpm = self.midi_parser.bpm
                print("Loaded file: " + filename)
                self.infoLine("Loaded: " + filename, 2)
            else:
                if not (filename.endswith('.mid') or filename.endswith('.midi')):
                    print("File is not a midi file: " + filename)
                    self.infoLine("Not a midi file: " + filename, 2)
                elif not (filename in self.filesystem):
                    print("File not found in filesystem: " + filename)
                    self.infoLine("File not found: " + filename, 2)
        except Exception as e:
            print("Error loading file: " + filename + " // " + str(e) + " // " + str(type(e)))
            print("Please check that this file is a midi file and is not corrupted.")
            self.infoLine("Error loading: " + filename, 2)
            self.infoLine("Ensure Midi File", 2)

    def changeFile(self, amount):
        self.checkMaxFiles()
        self.curFile += amount
        self.loadFile(self.filesystem[self.curFile])
        print("Changed file to: " + self.filesystem[self.curFile])

    def buttonUpdate(self):
        #if(self.input.currentlyPressed != None):
        #    print(self.input.currentlyPressed)
        self.key_event = self.macropad.keys.events.get()

        if self.input.encoderDown:
            if self.input.encoder_selection < self.fileAmt:
                self.loadFile(self.filesystem[self.curFile])
            else:
                print('File index out of range // No file loaded.')
                self.infoLine('File index out of range // No file loaded.', 2)

        if self.key_event:
            #print(self.key_event)
            if self.key_event.pressed:
                self.keysDown[self.key_event.key_number] = True

                #print(self.keysDown)

                if self.keysDown[9] and self.keysDown[11]: # if play and stop are pressed at the same time, enter channel select mode
                    self.typeMode = True
                    print("Entered channel select mode!")
                else:
                    self.typeMode = False

                if self.typeMode:
                    if self.key_event.key_number <= 8:
                        print("mrraow")
                else:
                    if self.key_event.key_number <= 8:
                        self.c1 = self.c2
                        self.c2 = (self.key_event.key_number + 1)
                    elif self.key_event.key_number == 10:
                        self.c1 = self.c2
                        self.c2 = 0

                    self.setChannel(self.combineSelection() - 1)

                    # if self.key_event.key_number == 9:
                    #     self.playing = True
                    #     print("Play button pressed!")
                    # elif self.key_event.key_number == 10:
                    #     self.playing = False
                    #     print("Stop button pressed!")
                    # elif self.key_event.key_number == 11:
                    #     self.player.stop()
                    #     self.player.play(loop=True)
                    #     print("Restart button pressed!")
            if self.key_event.released:
                self.keysDown[self.key_event.key_number] = False
                #print(self.keysDown)
            print(str(self.c1) + " : " + str(self.c2))
                    
        #if (self.input.currentlyPressed == 1):
        #    print("Button 2 pressed!")

    def displayUpdate(self):
        if self.curFile < self.fileAmt:
            self.filename = self.filesystem[self.curFile]
        else:
            self.filename = "[No file]"

        self.text_lines = self.macropad.display_text('File: ' + self.filename)
        self.text_lines[1].text = 'Channel: ' + str(self.combineSelection())
        self.text_lines[2].text = 'BPM: ' + str(self.bpm)
        self.macropad.display.refresh()
        self.text_lines.show()

    def infoLine(self, text, loopAmt=2):
        for i in range(loopAmt):
            self.text_lines[3].text = text
            self.macropad.display.refresh()
            time.sleep(0.5)
            self.text_lines[3].text = ""
            self.macropad.display.refresh()
            time.sleep(0.5)
        pass

    def combineSelection(self):
        print((self.c1 * 10) + self.c2)
        return (self.c1 * 10) + self.c2

    def playFile(self):
        print("Attempting to play file: " + self.filename)
        #self.infoLine("Playing: " + self.filename, 2)
        self.playing = True
        self.midi_parser.parse(self.filename)
        self.player.play(loop=True)
    
    def main(self):
        #self.playFile()
        self.playing = True
        self.setChannel(2)

        while True:
            
            self.input.checkInput()
            self.buttonUpdate()
            self.displayUpdate()
            
            
            if self.playing:
                self.player.play(loop=True)
            else:
                self.player.stop()
            
            #print("Encoder selection: " + str(self.input.encoder_selection))            
            
            self.curFile = self.input.encoder_selection
            self.elapsed += 1

app_instance = app()
app_instance.main()
