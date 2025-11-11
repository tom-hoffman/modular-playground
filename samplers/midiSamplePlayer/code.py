from app import SamplePlayerApp
import gc

app = SamplePlayerApp(15, 60)

gc.collect()
print("Free bytes after object def and creation = " + str(gc.mem_free()))

app.main()



