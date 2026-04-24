import cpx
import config

class ApplicationModel(object):
    '''This class should contain properties that store the state of the application.'''
    def __init__(self, 
                 millis_per_pulse=config.millis_per_pulse, 
                 pulses=0,
                 last_tap=None,
                 next_pulse=None,
                 photon=0,
                 active=True,
                 changed=True):
        self.millis_per_pulse = millis_per_pulse
        self.pulses = pulses
        self.last_tap = last_tap
        self.next_pulse = next_pulse
        self.photon = photon
        self.active = active
        self.changed = changed

    def advance_photon(self):
        self.photon = (self.photon + 1) % 10

    def update_millis(self, m):
        self.millis_per_pulse = cpx.ticks_diff(m, self.last_tap) // config.ppqn
        self.last_tap = m



