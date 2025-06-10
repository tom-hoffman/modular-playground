# Modular Playground

## Mission Statement(s)

### Meta-Pedagogical Mission

The broadest mission met by the Modular Playground is to create a long term, open ended project ecosystem for intermediate-level high school microcontroller programming and software product development.

#### Desirable characteristics:

  * The end product(s) should be usable *and engaging* to at least some high school and middle school students for real work/play.
  * Each module runs on standard, relatively inexpensive microcontroller development boards already widely owned by US schools.
  * Modules should interface with existing commercial and open source tools and products using standard protocols.
  * A student who has successfully completed AP Computer Science Principles should have the core programming competencies necessary to complete a module. 
  * The overall emphasis should remain on coding, optimizing use of microcontrollers already owned by the school, and minimizing non-reversible changes to the hardware (which may be needed for other classes/projects).
  * A competent small group of students should be able to *fully* complete a module in less than a semester.
  * A completed module/project should include not just coding and unit testing but integration testing with the rest of the system and external compatible tools, technical and end-user documentation.
  * Overall project documentation, publicity and promotion is integral to the process.
  * The project should demo well for both kids and adults.

### Practical Project Mission

To create modular (audio) synthesizers and modular synthesis components based on Adafruit's Circuit Playground Express (CPX) or Circuit Playground Bluefruit (CPB) microcontroller development boards.

The first step in this process is to create individual modules that interact with existing sythesizers and other modules, via MIDI primarily and secondarily through analog control and trigger voltages.  Example basic module types include: sequencers, oscillators, audio sample players, arpeggiators and MIDI utilities.  

#### What is the scope of the project?

There are a few types of projects encompassed by this project:

  * Modular Playground is an **open source software project**, that is, we're writing software to be freely shared under an open source software license, primarily though Github.
  * Modular Playground is a **synthesizer format**, specifying how compatible modules should interact and communicate with each other and how they can by physically mounted together to work as a single instrument.  Other sythesizer formats include Eurorack, Moog Unit (5U) and Kosmo.  In the compact tabletop synthesizer world, Korg's Volca series represents an example of a de-facto format.  The particulars of Modular Playground's format are based on the specifications of the CPX board.
  * Modular Playground is an **open source software distribution**, that is, a set of multiple pieces of open source software specifically modified and tested to work together reliably, particularly on specified hardware.  There are *many* microcontroller-based music synthesis projects that can be adapted with varying degrees of difficulty to work on the CPX and as part of a Modular Playground system.  This kind of adaptation and testing is very typical work in a professional environment.

#### Why Circuit Playground Express?

The first reason for basing this project on the CPX is that our school, like many other schools, libraries, maker spaces, etc., purchased class sets of them to teach the popular Code.org Computer Science Discoveries course and other similar curricula.  CS Discoveries specifically is widely taught in US middle and high schools.  In exploring and testing various approaches and microcontrollers, it became apparent that in addition to the wide availability there were some significant advantages to the Circuit Playground Express, despite the fact that on raw processing and memory terms, there are many more powerful microcontrollers available at lower prices.

##### Advantages:
  * We've already paid for them and have a set sitting in the closet most of the year.
  * Interesting user interface options for synthesizer modules:
    * Circle of 10 LED neopixels works great for common uses like displaying levels and sequencer steps.
    * RBG neopixels allow 3 or more layers of information simultaneously (e.g., blue shows sequence steps, green shows  triggers, red shows active step in sequence).
    * On board switch allows two-mode interface, e.g., performance mode is switch right and configuration mode is switch left, which works well as a standard for many modules., 
    * Two built in buttons are minimal but usually enough in combination with switch.
    * Up to 8 capacitive touch pads allow auxiliary button inputs (although somewhat slower and less reliable than the standard buttons).
    * Additional sensors allow development of a variety of interesting controllers (e.g., light-based theramin MIDI controller).
  * Excellent MIDI over USB (USB-MIDI) support in both Circuit Python and Arduino C++ (not true of all similar boards).
  * Built in 10-bit Digital to Analog Converter (DAC) for better audio quality (than relying on pulse wave modulation (PWM) without a DAC).
  * Great libraries and development environments in both Circuit Python and Arduino C++ supported by Adafruit, including web-based IDE's.
  * Good compatibility with the open source [Mozzi](https://sensorium.github.io/Mozzi/) C++ audio and synthesis library.

##### Disadvantages:
  * The CPX does not have a dedicated floating point unit (FPU) or other digital signal processing hardware that would allow high quality, low-latency audio effect processing.  
  * A wider range of voltage input and output (e.g., +5 volts) would give wider control voltage compatibility with Eurorack and other standard modules.
  * RAM is barely adequate for simple CircuitPython programming once necessary libraries for USB-MIDI, etc. are imported.

##### Design implications
This project starts from a unique starting point: *"Assume 15 microcontrollers..."*  In addition, each microcontroller is mounted on its own circular circuit board with its own buttons, switch and set of NeoPixels and LEDs.  

Let's say we are working on a sequencer.  In terms of computing power, a single CPX could easily run a very complex sequencer with many channels, steps and outputs.  Normally, one would add a variety of buttons, LEDs, other displays, etc. which would all be connected ultimately to a single microcontroller.  In the Modular Playground, the job of the sequencer would be split between multiple CPXs, not because of computational load, but to provide enough inputs and outputs for the user interface.  

For example, each CPX might represent a single track in an 8 step sequencer, so you would need four CPX for a four track sequencer with 8 steps.  From a normal cost perspective as a synth manufacturer or hobbyist this makes no sense -- you're using a 3 $30 boards in the place of maybe $2 in buttons and LEDs.  On the other hand, if the motivation is giving students a context in which to write highly modular code working in a real computing system, and being creative within a limited user interface, using hardware the school already owns, then it makes total sense.

#### What about the Circuit Playground Bluefruit?

##### Advantages of CPB over CPX:
  * Faster processor -- Cortex M4 vs. Cortex M0 for CPX.
  * More RAM -- particularly significant for Circuit Python programming.
  * Compatible with CircuitPython's powerful [synthio](https://docs.circuitpython.org/en/latest/shared-bindings/synthio/index.html#) library and a few others listed below. (CPX does not have enough RAM).
  * Bluetooth for wireless communication and [Bluetooth MIDI](https://docs.circuitpython.org/projects/ble_midi/en/latest/).
  * Currently the same price for a single unit as CPX ($24.95 as of 6/10/2025).

##### Disadvantages of CPB vs. CPX:
  * Not sold in class sets for Code.org and other curricula so unlikely to already be lying around in large numbers.
  * Buying 15 individual CPB is more expensive than a [class set of CPX](https://www.adafruit.com/product/3399).
  * No hardware DAC output pin; the "audio" pin provides high frequency pulse width modulation but not true DAC.

##### How compatible is code between the two?
It *seems* like most CPX code should be forward compatible to the CPB, particularly in CircuitPython, but at this early point, I don't think any promises should be made about universal compatibility with CPB.  I would regard this as a good task for year two or three of the project: doing compatibility testing and considering whether an abstraction layer is necessary or desirable to smooth out any issues in CircuitPython or C++.  I would consider forward compatibility to be a premature optimization in starting this project.

##### Where would dedicated CPB hardware modules be potentially useful?

  1. Providing a bridge to external Bluetooth MIDI devices, particularly tablets and smartphones.
  2. CircuitPython modules making specific use of:
      * [synthio](https://docs.circuitpython.org/en/latest/shared-bindings/synthio/index.html#)
      * [audiomixer](https://docs.circuitpython.org/en/latest/shared-bindings/audiomixer/index.html)
      * [audiomp3](https://docs.circuitpython.org/en/latest/shared-bindings/audiomp3/index.html)

We do encourage deveopers to get the most out of the CPX before jumping to CPB.

#### What about the Circuit Playground Classic?
Most importantly, the Circuit Playground Classic (CPC) does not support CircuitPython at all, so that will exclude many if not most modules going forward.  Arduino C++ programs *may* work, but backward compatibility is not a priority at the start of this project.  The CPC is a bit cheaper purchased individually at [$19.95](https://www.adafruit.com/product/3000) (as of 6/10/2025), but it is hard to imagine people are still purchasing a lot of these, and my impression is that there are many more CPX in the field than CPC.  Again, down the road some compatibility testing would be a good project for some students.

#### What about (my favorite microcontroller board)!?!?
(Your favorite microcontroller board) is awesome!  You should make some modules that communicate with Modular Playground modules using USB-MIDI!  However, those awesome modules will be separate projects.  Modular Playground is for Circuit Playground Expresses and occasionally Circuit Playground Bluetooths (blueteeth?), which share the same form factor and quirky but flexible user interface.

  [a complete system or part of a system with 3rd party components using standard protocols and formats]

#### Guidelines
  * USB-MIDI is the preferred means of communication between components.
  * No components should be directly soldered, but custom jacks/connectors may need to be soldered to wires, crimping is acceptible if effective in a given case.  Nothing should be permanently attached to a Circuit Playground.
  * Each module should be fully functional with only the sensors, LEDs and buttons integrated into the CPX (that is, not depending on wiring up additional buttons, etc.).
  * For enhanced monitoring modules using a LCD, the Adafruit TFT Gizmo is recommended.
  * Circuit Python and Arduino IDE C++ are both acceptable, with Circuit Python preferred when it offers sufficient performance.
  * For C++ projects, the Mozzi synthesis library is recommended.
  * No part of the project should depend on digital audio workstation (DAW) components.

### Additional hardware needed
In Modular Playground, USB provides both power and MIDI connectivity to the CPX in a single cable.  In testing this has proven to be reliable and robust.  This requires the following additional hardware:
  1. **USB hub**:  For a reliable setup, we recommend a powered USB 2 or 3 hub with 10 or 15 ports.  These are commonly available on Amazon and similar sources for $30 - $80.  Separate power buttons on the hub are a nice but not essential feature.  Make sure it supports *data* transfer, not just power.    
  1. **PC as USB host**:  There are a few options here:
        * In theory, any Windows, Mac, or Linux PC can be configured to act as the host for USB-MIDI communications.  In practice, this process can fail silently for a variety of reasons and will prevent any communication at all between the CPX modules.  We don't recommend starting this way until the correct process can be fully documented.
        * Most sites that already have a set of Circuit Playgrounds probably also have a stash of Rasberry Pi's, and a Pi 3 or greater can act as a USB MIDI host.  There are clear instructions online for setting up a Pi running Linux as a USB-MIDI host which have proven to be very reliable.  The Pi is small enough that it can fit alongside the CPXs on a board or in a case to create a self-contained instrument (i.e., you don't also have to plug the whole thing into a laptop).  In the long run, an advanced project would be to manage the software on the set of connected CPX's through the Raspberry PI through a web interface, for example, by assigning specific roles (MIDI clock, step sequencer, bass drum) to each CPX.
        * Some microcontroller boards, such as the Arduino Due or Adafruit Metro RP2350 can act as USB hosts, but this has not been tested or documented by us and the price difference between these boards and a Raspberry Pi 3 or 4 does not seem to be worth the bother, but this is another topic for additional study and testing.
