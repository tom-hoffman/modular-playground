* Installing Circuit Python (for Circuit Playground).
  * Go here: https://circuitpython.org/board/circuitplayground_express/
  * Download the 9.x version of CircuitPython (.uf2).
  * If a dialog comes up, you *can* download that directly to the CPLAYBOOT drive.
  * Otherwise, you will need to drag the .uf2 file from your Downloads file to the CPLAYBOOT drive.
  * If the CPLAYBOOT drive does not come up and the neopixels are not a steady green, 
    click the RESET button on the Circuit Playground.
  * After the download, the Circuit Playground should unmount and remount as CIRCUITPY.
  * At this point the NeoPixels should rapidly flash yellow three times, and then 
    occasionally give a quick green flash.
* Development Environment(s)
  * For school: use https://code.circuitpython.org/
    * Note that each of these steps might take 0 - 15 seconds.  Be (somewhat) patient.
    * Connect your Circuit Playground using USB.
    * After you click CONNECT and USB, you should see a dialog which has 
      "CircuitPython CDC Connect (COMxx) - Paired"
      as an option.  Select that one, and click [Connect].
    * If this is working, you should see a spinning Python animation (ouroboros),
      and the neopixels will turn white.
    * Then select the CIRCUITPY drive as the "host folder."
  * For Ubuntu: DON'T use https://code.circuitpython.org!!! (not sure why it doesn't work)
    * Bare Text Editor and `screen` in the terminal seems to be the way to go.  If it doesn't work it doesn't work directly!
    * Serial connection with `screen /dev/ttyACM0 115200`
    * This incantation might help, from the repl:
        ```
        import storage
        storage.erase_filesystem()
        ```
* Downloading and unzipping Project Bundles from Adafruit
  * Change your browser settings (if necessary):
    * Go to Settings > Downloads
    * Turn ON: `Ask where to save each file before downloading`
    * For the save location choose your network drive as indicated below.
  * You need to download files to your NETWORK DRIVE.
  * This is INSIDE "MY COMPUTER" (which makes no sense).
  * It is named after your student ID number and is the `H:` drive.
  * These files can then be used from any Windows PC in the school (or district).
* Useful links:
  * [Adafruit docs](https://docs.circuitpython.org/en/latest/README.html)
  * [Audio out tutorial](https://learn.adafruit.com/adafruit-circuit-playground-express/circuitpython-audio-out)
  * [Microcontroller Compatible Audio File Conversion
](https://learn.adafruit.com/microcontroller-compatible-audio-file-conversion)
  * [Memory saving tips](https://learn.adafruit.com/Memory-saving-tips-for-CircuitPython/overview)
  * [todbot Tricks (esp. `synthio`)](https://github.com/todbot/circuitpython-tricks)
