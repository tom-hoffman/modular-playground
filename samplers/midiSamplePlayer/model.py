
class PlayerModel(object):
    def __init__(self, bank_button_count=0, bank_cc_count=0, 
                 sample_button_count=0, sample_cc_count=0,
                 wav=None):
        self.bank_button_count = bank_button_count
        self.bank_cc_count = bank_cc_count
        self.sample_button_count = sample_button_count
        self.sample_cc_count = sample_cc_count
        self.wav = wav

