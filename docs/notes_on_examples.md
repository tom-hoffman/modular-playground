Circuit Playground/CircuitPython Example Notes
==============================================

These are specifically relevant to Modular Playground and Computer Music Workshop needs.  
There are many relevant examples online and some need a little tweaking to work on our setup.

CircuitPython Audio Out (Adafruit)
----------------------------------

https://learn.adafruit.com/adafruit-circuit-playground-express/circuitpython-audio-out

Additional libraries: none; Works out of the box: yes; Tweakability: iffy.

### First Example

The basic 440hz A sine wave works, but this isn't as easily modified as implied by a quick read of the code.

To use any frequency you need to prevent slight overflows for some values, using `min()`: 

`    sine_wave[i] = min(int(math.sin(math.pi * 2 * i / length) * (2 ** 15) + 2 ** 15), 65535)`

Changing the `SAMPLERATE` does not leave the frequency unchanged, so it isn't a quick way to demonstrate changing the sample rate of a digital waveform.
