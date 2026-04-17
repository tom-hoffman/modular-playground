import config

class ApplicationModel(object):
    '''This class should contain properties that store the state of the application.'''
    def __init__(self, millis_per_pulse=config.millis_per_pulse, changed=True):
        self.changed = changed
        self.millis_per_pulse = millis_per_pulse



