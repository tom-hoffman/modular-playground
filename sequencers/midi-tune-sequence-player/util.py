

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

def note_parser(midstr):
    if midstr == 0:
        return None
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
