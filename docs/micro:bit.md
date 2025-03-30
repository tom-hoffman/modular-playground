micro:bit notes
===============

In addition to the Circuit Playground, the "other" widely used microcontroller board used in classrooms is the BBC micro:bit.  I've been focusing on the Circuit Playground but also am fortunate to have a couple class sets of micro:bits.  For someone who is not an expert in these devices, working out the differences between the two, for music making and synthesis in particular, are complex.

| Feature            | Circuit Playground                     | micro:bit v2                                   |
|--------------------|----------------------------------------|------------------------------------------------|
| SoC                | ATSAMD21G18                            | nRF52833                                       |
| CPU                | ARM Cortex M0                          | ARM Cortex M4 with FPU (floating point math)   |
| Max. clock speed   | 48 Mhz                                 | 64 MHz                                         |
| RAM                | 32K                                    | 128K                                           |
| Flash memory       | 256K                                   | 512K                                           |
| Makecode           | https://makecode.adafruit.com/         | https://makecode.microbit.org/#editor          |
| Basic sound & music| yes                                    | yes                                            |
| Synthesis blocks   | no                                     | yes!!!                                            |
| MIDI out blocks    | no                                     | yes (via extension); limited Bluetooth out     |
| MIDI in blocks     | no                                     | no                                             |
| Recording blocks   | no                                     | yes (via extension                             |








MakeCode Extensions and TypeScript
----------------------------------

[MakeCode extensions](https://makecode.com/extensions) seem to be almost entirely TypeScript which compiles to machine code (essentially).  For example, [pxt-midi](https://github.com/microsoft/pxt-midi/tree/master), which sends MIDI messages over serial, only has one tiny .cpp extension for performance.  

The approach taken to MIDI in micro:bit MakeCode is a bit puzzling, I think because it is written almost entirely in terms of sending MIDI messages to software instruments on a PC (thus the constant references to using Hairless MIDI).  Adding USB MIDI is probably not that hard but a lot to initially wrap one's head around.

All things considered, unlocking MakeCode's excellent synthesis blocks with some MIDI input blocks is maybe a smarter move than, say, [getting Mozzy running on micro:bit's SAMD51(?) chip](https://diyelectromusic.com/2021/04/16/samd-usb-midi-multi-pot-mozzi-synthesis/).
