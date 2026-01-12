Modular Playground ByteBeat Oscillator
======================================

Bytebeat traditionally has been done in C or Javascript (which shares a lot of syntax with C). 
Some C and Javascript bytebeat will "just work" in Python, some will need code modification to work in Python.

C/Javascript operators that work directly in Python:
----------------------------------------------------

* math: `+ - * / % **`
* binary operators: `& | ^ << >>`
* assignment `= += -= *= /= %=`

Trig. functions:
----------------
To use `cos`, `sin`, `tan` etc., do the following import at the beginning of your code:

`from math import *`

Modifications:
--------------

* increment and decrement: `++` and `--` may work in Python as `+= 1` and `-= 1`.

Complications:
----------------

When brackets `[]` are sprinkled through the code, these are probably used as list or string indexes.  
The syntax is the same in all relevant languages so it *might* work without change, but probably indicates
enough complexity that something else will need adjustment.

When the code is wrapped in brackets `[]` it seems to be outputting a list of stereo values as a list.  
Probably we can directly use one of those elements.  They should be separated by a comma.  I'd avoid these
until we're more comfortable.

To do:
------

* Try a bunch of bytebeat functions.
* Get a sense of which work.
* Figure out the timing of the default loop.  Use a `for` loop instead of `while` to see how long it takes for, say 1,000,000 iterations.
  
