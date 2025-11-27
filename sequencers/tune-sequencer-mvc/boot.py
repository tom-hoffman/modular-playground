# sets the name of the Circuit Playground as it appears to a PC
# from https://github.com/todbot/circuitpython-tricks#usb

# customize name here:
name = "YIELD"

import storage
storage.remount("/", readonly=False)
m = storage.getmount("/")
m.label = name
storage.remount("/", readonly=True)
