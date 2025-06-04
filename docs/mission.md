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

To create modular (audio) synthesizers and modular synthesis components based on Adafruit's Circuit Playground microcontrollers.

#### Why Circuit Playgrounds?

The first reason for basing this project on the Circuit Playground is that our school purchased class sets of them to teach the popular Code.org Computer Science Discoveries course.  This course is widely taught in US middle and high schools.  In exploring and testing various approaches and microcontrollers, it became apparent that there were some significant advantages to the Circuit Playground, despite the fact that on raw processing and memory terms, there are many more powerful microcontrollers available at lower prices.

Advantages:
  * We've already paid for them and have a set sitting in the closet most of the year.
  * Interesting user interface options for synthesizer modules:
    * Circle of 10 LED neopixels works great for common uses like displaying levels and sequencer steps.
    * RBG neopixels allow 3 or more layers of information simultaneously (e.g., blue shows sequence steps, green shows  triggers, red shows active step in sequence).
    * On board switch allows two-mode interface, e.g., performance mode is switch right and configuration mode is switch left, which works well as a standard for many modules.
    * Two built in buttons are minimal usually enough in combination with switch.
    * 
  * Excellent MIDI over USB (USB-MIDI) support in both Circuit Python and Arduino C++ (not true of all similar boards).
  * 

[a complete system or part of a system with 3rd party components using standard protocols and formats]


#### Guidelines
  * USB-MIDI is the preferred means of communication between components.
  * No components should be directly soldered, but custom jacks/connectors may need to be soldered to wires, crimping is acceptible if effective in a given case.  Nothing should be permanently attached to a Circuit Playground.
  * Each module should be fully functional with only the sensors, LEDs and buttons integrated into the Circuit Playground (that is, not depending on wiring up additional buttons, etc.).
  * For enhanced monitoring modules using a LCD, the Adafruit TFT Gizmo is recommended.
  * Circuit Python and Arduino IDE C++ are both acceptable, with Circuit Python preferred when it offers sufficient performance.
  * For C++ projects, the Mozzi synthesis library is recommended.
  * No part of the project should depend on digital audio workstation (DAW) components.


