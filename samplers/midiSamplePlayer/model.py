class PlayerModel(object):
    def __init__(self, channel, note, sample_index=0, bank_index=0, 
                 wav_file=None, wav=None, midi=None):
        self.channel = channel
        self.note = note
        self.sample_index = sample_index
        self.bank_index = bank_index
        self.wav_file = wav_file
        self.wav = None
        self.midi = MinimalMidi(channel, None)
        self.msg = None