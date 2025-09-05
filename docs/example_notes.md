Circuit Playground/CircuitPython Example Notes
==============================================

These are specifically relevant to Modular Playground and Computer Music Workshop needs.  
There are many relevant examples online and some need a little tweaking to work on our setup.

CircuitPython Audio Out (Adafruit)
----------------------------------

https://learn.adafruit.com/adafruit-circuit-playground-express/circuitpython-audio-out

Additional libraries: none; Works out of the box: yes; Tweakability: high.

To use any frequency you need to prevent slight overflows for some values, using `min()`: 

`    sine_wave[i] = min(int(math.sin(math.pi * 2 * i / length) * (2 ** 15) + 2 ** 15), 65535)`


