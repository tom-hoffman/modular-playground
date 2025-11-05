
import gc
gc.collect()
print("Starting free bytes (after gc) = " + str(gc.mem_free()))
    
from app import SamplePlayerApp

app = SamplePlayerApp()

app.main()

