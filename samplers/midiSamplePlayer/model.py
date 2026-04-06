# note that his is not actually used yet.

class PlayerModel(object):
    def __init__(self, channel, note, sample_index=0, bank_index=0, 
                 wav_file=None, wav=None, midi=None, current_cc=0):
        self.channel = channel
        self.note = note
        self.sample_index = sample_index
        self.bank_index = bank_index
        self.wav_file = wav_file
        self.wav = None
        self.midi = MinimalMidi(channel, None)
        self.msg = None
        self.current_cc = current_cc