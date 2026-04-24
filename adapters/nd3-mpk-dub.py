# nd3-mpk-dub.py

# A USB-MIDI adapter that listens for MIDI messages from the MPKminiplus (MPK)
# and translates them for multi-channel use on a Nord Drum 3p (ND3).

# Specifically, the ND3 can listen on seven channels, one for each drum
# and one for global messages.  The programmable controls on the MPK can
# only be addressed to one channel, so this script will allow the 
# adapter to route messages to multiple channels on the ND3.

# copyright Tom Hoffman 2026.

# NOTES:
# Using 1-16 for MIDI channel range (as displayed).

import usb_midi
from micropython import const

# for the MPK outgoing messages
# based on the default Program 1 (named MPC)

_MPK_KEY_OUT_CH = const(1)
_MPK_PAD_OUT_CH = const(10)

# {control ID on device : MIDI CC number}
CONTROLLER_CODES = {
    # pads
    # red bank
    'PAD1' : 16,
    'PAD2' : 17,
    'PAD3' : 18,
    'PAD4' : 19,
    'PAD5' : 20,
    'PAD6' : 21,
    'PAD7' : 22,
    'PAD8' : 23,
    # green bank
    'PAD9' : 24,
    'PAD10' : 25,
    'PAD11' : 26,
    'PAD12' : 27,
    'PAD13' : 28,
    'PAD14' : 29,
    'PAD15' : 30,
    'PAD16' : 31,
    # knobs
    'K1' : 70,
    'K2' : 71,
    'K3' : 72,
    'K4' : 73,
    'K5' : 74,
    'K6' : 75,
    'K7' : 76,
    'K8' : 77,
    # joystick
    'JOYX1' : 12,
    'JOYX2' : 13,   # modify on MPK
    'JOYY1' : 14,   # modify on MPK
    'JOYY1' : 15,
    # transport keys (all send 127)
    '<<' : 115,
    '>>' : 116,
    'STOP' : 117,
    'PLAY' : 118,
    'REC' : 119
}
