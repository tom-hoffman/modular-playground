# Modular Playground

## Mission Statement(s)

### Meta-Pedagogical Mission

The broadest mission met by the Modular Playground is to create a long term, open ended project ecosystem for intermediate-level high school microcontroller programming and software product development.

#### Desirable characteristics:

  * The end product(s) should be usable *and engaging* to at least some high school and middle school students for real work/play.
  * Each module runs on standard, relatively inexpensive microcontroller development boards already widely owned by US schools.
  * Modules should interface with existing commercial and open source tools and products using standard protocols.
  * The coding skills needed to contribute a genuinely useful module is within reach of a student who has successfully completed AP Computer Science Principles.
  * The overall emphasis must remain on coding, optimizing use of microcontrollers already owned by the school, and minimizing non-reversible changes to the hardware (which may be needed for other classes/projects).
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

#### Why Circuit Playground?

The first reason for basing this project on the CPX is that our school purchased class sets of them to teach the popular Code.org Computer Science Discoveries course.  This course is widely taught in US middle and high schools.  In exploring and testing various approaches and microcontrollers, it became apparent that there were some significant advantages to the Circuit Playground, despite the fact that on raw processing and memory terms, there are many more powerful microcontrollers available at lower prices.

Advantages:
  * We've already paid for them and have a set sitting in the closet most of the year.
  * Interesting user interface options for synthesizer modules:
    * Circle of 10 LED neopixels works great for common uses like displaying levels and sequencer steps.
    * RBG neopixels allow 3 or more layers of information simultaneously (e.g., blue shows sequence steps, green shows  triggers, red shows active step in sequence).
    * On board switch allows two-mode interface, e.g., performance mode is switch right and configuration mode is switch left, which works well as a standard for many modules.
    * Two built in buttons are minimal but usually enough in combination with switch.
    * Up to 8 capacitive touch pads allow auxiliary button inputs (although somewhat slower and less reliable than the standard buttons).
    * Additional sensors allow development of a variety of interesting controllers (e.g., light-based theramin MIDI controller).
  * Excellent MIDI over USB (USB-MIDI) support in both Circuit Python and Arduino C++ (not true of all similar boards).
  * Built in 10-bit Digital to Analog Converter (DAC) for better audio quality (than relying on pulse wave modulation (PWM) without a DAC).
  * Great libraries and development environments in both Circuit Python and Arduino C++ supported by Adafruit, including web-based IDE's.
  * Good compatibility with the open source [Mozzi](https://sensorium.github.io/Mozzi/) C++ audio and synthesis library.

Disadvantages:
  * The CPX does not have a dedicated floating point unit (FPU) or other digital signal processing hardware that would allow high quality, low-latency audio effect processing.  
  * A wider range of voltage input and output (e.g., +5 volts) would give wider control voltage compatibility with Eurorack and other standard modules.
  * RAM is barely adequate for simple CircuitPython programming once necessary libraries for USB-MIDI, etc. are imported.

[a complete system or part of a system with 3rd party components using standard protocols and formats]

#### Guidelines
  * USB-MIDI is the preferred means of communication between components.
  * No components should be directly soldered, but custom jacks/connectors may need to be soldered to wires, crimping is acceptible if effective in a given case.  Nothing should be permanently attached to a Circuit Playground.
  * Each module should be fully functional with only the sensors, LEDs and buttons integrated into the CPX (that is, not depending on wiring up additional buttons, etc.).
  * For enhanced monitoring modules using a LCD, the Adafruit TFT Gizmo is recommended.
  * Circuit Python and Arduino IDE C++ are both acceptable, with Circuit Python preferred when it offers sufficient performance.
  * For C++ projects, the Mozzi synthesis library is recommended.
  * No part of the project should depend on digital audio workstation (DAW) components.


