
import gc
gc.collect()
print("Starting free bytes (after gc) = " + str(gc.mem_free()))
    
from app import SamplePlayerApp

channel = 15
note = 60

app = SamplePlayerApp(channel, note)

gc.collect()
print("Free bytes after setup = " + str(gc.mem_free()))

app.main()

