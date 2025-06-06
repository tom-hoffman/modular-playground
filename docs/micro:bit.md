micro:bit notes
===============

In addition to the Circuit Playground, the "other" widely used microcontroller board used in classrooms is the BBC micro:bit.  I've been focusing on the Circuit Playground, but also am fortunate to have a couple class sets of micro:bits.  For someone who is not an expert in these devices, working out the differences between the two, for music making and synthesis in particular, are complex.

This overall analysis is slanted toward music and audio synthesis and processing.

| Feature            | Circuit Playground                     | micro:bit v2                                   |
|--------------------|----------------------------------------|------------------------------------------------|
| SoC                | ATSAMD21G18                            | nRF52833 (ATSAMD51?)                           |
| CPU                | ARM Cortex M0                          | ARM Cortex M4                                  |
| FPU & DSP hardware | **NO**                                 | **YES**                                        |
| Max. clock speed   | 48 Mhz                                 | 64 MHz                                         |
| RAM                | 32K                                    | 128K                                           |
| Flash memory       | 2 MB                                   | **512K**                                       |
| DAC                | 10-bit, pin A0                         | **NO**                                         |
| I2S                | no                                     | no                                             |
| favored Python     | CircuitPython                          | MicroPython                                    |
| Arduino IDE        | Plug and play                          | a more work to set up, fewer examples, etc     |
| Mozzi C++ library  | works                                  | reportedly works with a fair bit of setup      |
| Makecode           | https://makecode.adafruit.com/         | https://makecode.microbit.org/#editor          |
| Basic sound & music| yes                                    | yes                                            |
| Synthesis blocks   | no                                     | **YES!!!**                                     |
| MIDI out blocks    | no                                     | yes (via extension); limited Bluetooth out     |
| MIDI in blocks     | no                                     | no                                             |
| Recording blocks   | no                                     | yes (via extension)                            |

References:
* [micro:bit with Arduino setup](https://learn.adafruit.com/use-micro-bit-with-arduino/overview)
* [micro:bit with Mozzi synth library](https://diyelectromusic.com/2021/04/16/samd-usb-midi-multi-pot-mozzi-synthesis/)
* [MicroPython USB MIDI example](https://github.com/micropython/micropython-lib/blob/master/micropython/usb/examples/device/midi_example.py)

USB MCU & MIDI
--------------

Both microcontrollers use a separate processor to handle USB communications.  This is a bit deep in the weeds for me, but the issue is that the USB MCU used by micro:bit (or some component closely related to it) is not supported by the most common Arduino/C++ USB-MIDI implementations.  If there is a workaround it is not obvious.  

In short, no MIDI-USB on Arduino/C++.

Advantages of micro:bit vs. Circuit Playground
----------------------------------------------

* faster CPU clock **and** dedicated floating point and digital signal processing;
* 4x more RAM (but flash space is limiting for MicroPython modules);
* great API support for audio synthesis in MakeCode and MicroPython;
* nice self-contained Python libraries (esp. built into web editor);
* very easy Bluetooth/radio connection between micro:bits.

Advantages of Circuit Playground vs. micro:bit
----------------------------------------------
* Digital to audio conversion (DAC) pin -- should be higher fidelity than PWM on micro:bit;
* USB MIDI support in CircuitPython and Arduino/C++
* more flash allows more CircuitPython libraries;
* more flexible, expressive and compelling user interface with RGB neoPixels;
* an onboard switch in addition to buttons allows more input flexibility;
* more capacitive touch points for more input options;
* all pins are more physically accessible without breakout board;
* better supported/documented in Arduino IDE;

MicroPython vs. CircuitPython audio notes
-----------------------------------------

Both MicroPython and CircuitPython should run on both boards. The micro:bit team favors MicroPython and the Circuit Playground's creators at Adafruit also developed CircuitPython, so those two work together seamlessly. Both language variants also have nice web based editors.

MakeCode Extensions and TypeScript
----------------------------------

[MakeCode extensions](https://makecode.com/extensions) seem to be almost entirely TypeScript which compiles to machine code (essentially).  For example, [pxt-midi](https://github.com/microsoft/pxt-midi/tree/master), which sends MIDI messages over serial, only has one tiny .cpp extension for performance.  

The approach taken to MIDI in micro:bit MakeCode is a bit puzzling, I think because it is written almost entirely in terms of sending MIDI messages to software instruments on a PC (thus the constant references to using Hairless MIDI).  Adding USB MIDI is probably not that hard but a lot to initially wrap one's head around.
