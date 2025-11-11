from midi_config_mode import MidiConfigMode
from sample_select_mode import SampleSelectMode
import gc

print("Starting Sample Player...")

app = SampleSelectMode(15, 60)
app.changeSample()
app.updatePixels()
app.midi.clear_msgs()

app.main()




