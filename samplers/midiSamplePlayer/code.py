from midi_config_mode import MidiConfigMode
from sample_select_mode import SampleSelectMode

import config

print("Starting Sample Player...")

app = SampleSelectMode(config.channel_in, config.)
app.changeSample()
app.updatePixels()
app.midi.clear_msgs()

app.main()

while True:
    for i in range(config.MIDI_READ_REPEAT):
        app.main()
    app.updateButtons()
    app.checkButtons()



