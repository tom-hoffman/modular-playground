from midi_config_mode import MidiConfigMode
from sample_select_mode import SampleSelectMode


print("Starting Sample Player...")

CHANNEL = 5
NOTE = 36

app = SampleSelectMode(CHANNEL, NOTE)
app.changeSample()
app.updatePixels()
app.midi.clear_msgs()

app.main()

_button_delay = 0

while True:
    if _button_delay == 512:
        app.updateButtons() 
        app.checkButtons()
        _button_delay = 0
    else:
        _button_delay += 1
    app.main()


