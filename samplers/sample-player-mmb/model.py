
import config
import os
from audiocore import WaveFile

class PlayerModel(object):
    def __init__(self, bank_button_count=0, bank_cc_count=0, 
                 sample_button_count=0, sample_cc_count=0,
                 cc_keys=[], wav=None):
        self.bank_button_count = bank_button_count
        self.bank_cc_count = bank_cc_count
        self.sample_button_count = sample_button_count
        self.sample_cc_count = sample_cc_count
        self.cc_keys = list(config.CC_VALUES)
        self.wav = wav
        self.update_display = False

    def calculate_sample_index(self) -> int:
        return (self.sample_button_count + self.sample_cc_count) % len(config.BANKS)

    def calculate_bank_index() -> int:
        return (self.bank_button_count + self.bank_cc_count) % config.SAMPLE_COUNT

    def change_sample(self):
        path = config.BANKS[self.calculate_bank_index] + '/' + str(self.calculate_sample_index)
        fileName = os.listdir(path)[0]
        self.wav_file = open(path + '/' + fileName, 'rb')
        self.wav = WaveFile(self.wav_file)