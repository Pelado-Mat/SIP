SIP
====

An improved Python port of the Arduino based OpenSprinkler firmware, originally based on V 1.8.3 and updated by Dan Kimberling using the power of Python.

This fork attempt to encapsulate the control logic from the main program in plugins, to enable a simpler way to implement diferent HW configurations. 

My driver is the need to program a irrigation from a pond, in a rural enviroment. I must control a pump, 16 valves and be sure that our tank has water.

I will be using a [simple water level sensor from ICS](http://www.icstation.com/icstation-water-level-sensor-module-arduino-stm32-p-3258.html) to shutdown everything if we reach the desired water level.
To control the valves I'm planning to use a couple of relays with the [relay_board plugin](https://github.com/KanyonKris/relay_board)


-----------------------------------------------------------------

GNU GPL License<br/>
December 2015


***********
UPDATES 
===========

***********
December 11 2015
----------
(MatiasV)
1. Just fork Dan work and start working on the ControlPlugin Branch


NOTE
====
This folder contains a fork of OpenSprinkler Pi written by Dan Kimberling using Python as it should be used. It is largly compatible with the microcontroller-based OpenSprinkler firmware 1.8, the instructions of which can be found at:
  
  http://rayshobby.net/?page_id=730

The program makes use of web.py (http://webpy.org/) for the web interface. 

******************************************************
Full credit goes to Dan for his generous contributions
in porting the microcontroller firmware to Python.
******************************************************

================================================================

## Installation and set up
Just follow DAN instructions...
https://github.com/Dan-in-CA/SIP/

