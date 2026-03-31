# minimal_midi.py — Optimized for MIDI clock transmission only

import usb_midi
from micropython import const

_CLOCK = const(b'\xF8')  # System Real-Time Clock message (0xF8)

def send_clock(port):
    """Send a single MIDI clock pulse through the given USB MIDI port."""
    port.write(bytes([_CLOCK]))


# Initialize output-only port for clock transmission
_OUTIE = usb_midi.ports[1]  # PortOut is at index 1 in ports tuple


# Helper function that can be called from main code (no class needed)

def send_clock_now():
    """Send a MIDI clock message immediately."""
    send_clock(_OUTIE)


# Optional: MinimalMidi wrapper if you need to reuse this interface elsewhere
class MinimalMidi:
    """Minimal MIDI clock sender for tap tempo applications."""

    def __init__(self, port_out=None):
        self.out = port_out or _OUTIE  # Default to pre-initialized output port

    def send(self):
        """Send a single MIDI clock pulse."""
        self.out.write(bytes([_CLOCK]))


# Usage notes:
# - This module only sends MIDI clock (0xF8), no input handling needed
# - Memory footprint reduced by removing unused methods and constants
# - Direct .write() calls ensure maximum responsiveness on CPX
