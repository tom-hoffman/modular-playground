import usb_midi         # basic MIDI over USB support




import cpx

CLOCK_MSG = b'\xF8'
NOTE_ON_MESSAGES = bytes(range(144, 160))
NOTE_OFF_MESSAGES = bytes(range(128, 144))

innie = usb_midi.ports[0]
outie = usb_midi.ports[1]

NOTE_DURATIONS = {'32n' : 3,
                  '16n' : 6,
                  '8n' : 12,
                  '4n' : 24,
                  '2n' : 48,
                  '1n' : 96,
                  '1dn' : 144,
                  '2dn' : 72,
                  '4dn' : 36,
                  '8dn' : 18}


# from https://stackoverflow.com/questions/13926280/musical-note-string-c-4-f-3-etc-to-midi-note-value-in-python

def midiStringToInt(midstr):
    Notes = [["C"],["C#","Db"],["D"],["D#","Eb"],["E"],["F"],["F#","Gb"],["G"],["G#","Ab"],["A"],["A#","Bb"],["B"]]
    answer = 0
    i = 0
    #Note
    letter = letter = midstr[:-1]
    for note in Notes:
        for form in note:
            if letter.upper() == form:
                answer = i
                break;
        i += 1
    #Octave
    answer += (int(midstr[-1]))*12
    return answer


def getTune(notes, index):
    return notes[index]

def getNotePair(tune, index):
    # Returns (pitch, duration) from the notes tuple.
    return tune[index]

def getPitch(tune, index):
    note_pair = getNotePair(tune, index)
    pitch_text = note_pair[0]
    return midiStringToInt(pitch_text)

def getDuration(tune, index):
    note_pair = getNotePair(tune, index)
    note_text = note_pair[1]
    return NOTE_DURATIONS[note_text]

class SequencePlayerApp(object):
    def __init__(self, channel, notes):
        self.channel = channel
        self.notes = notes
        self.tuneIndex = 0
        self.clockCount = 0
        self.noteIndex = 0
        self.tune = getTune(self.notes, self.tuneIndex)
        self.pitch = getPitch(self.tune, self.noteIndex)
        self.duration = getDuration(self.tune, self.noteIndex)
        self.playing = False

    def updatePixels(self):
        cpx.pix.fill((32, 0, 32))
        cpx.pix[self.tuneIndex] = (0, 32, 0)
        cpx.pix.show()

    def updateTune(self):
        self.noteIndex = 0
        self.clockCount = 0
        self.tune = getTune(self.notes, self.tuneIndex)
        self.pitch = getPitch(self.tune, self.noteIndex)
        self.duration = getDuration(self.tune, self.noteIndex)
        self.playing = False
        self.updatePixels()

    def checkButtons(self):
        cpx.a_button.update()
        cpx.b_button.update()
        if cpx.a_button.rose:
            self.tuneIndex -= 1
        if cpx.b_button.rose:
            self.tuneIndex += 1

    def main(self):
        self.updatePixels()
        while True:
            self.checkButtons()
            msg_in = innie.read(1)
            print(msg_in)
            if msg_in:

                if msg_in == CLOCK_MSG:
                    if self.clockCount >= self.duration - 1:
                        self.clockCount = 0
                        cpx.led.value = not(cpx.led.value)
                        self.noteIndex = self.noteIndex + 1
                        if self.noteIndex >= len(self.tune):
                            self.noteIndex = 0
                        self.pitch = getPitch(self.tune, self.noteIndex)             
                        if self.pitch:
                            self.duration = getDuration(self.tune, self.noteIndex)
                            outie.write(bytes[NOTE_ON_MESSAGES[self.channel]])
                            outie.write(bytes([self.pitch, 127]))
                            self.playing = True
                        else:
                            pass
                            #midi.send(NoteOff(self.pitch, 0))
                    else:
                        self.clockCount = self.clockCount + 1
                        if self.playing:
                            #midi.send(NoteOff(self.pitch, 0))
                            self.playing = False
