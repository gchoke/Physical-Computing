This project will be used to store and share python commands developed for the
Raspberry Pi. 

morse.py is intended to run on a raspberry pi.
It converts a text message to morse code.  
It can be run from a terminal session or Idle
Python 3 is assumed
The program uses parallel lists letters, and codes to store the letters and
morse code encryptions.

The gpiozero module is used to create an instance of LED on GPIO port 17.
It necessary to hook up an led with a current limiting resistor on that pin.
Created by Greg Hoke on 5/12/2017 as an assignment for an RPi 
Physical Computing Course. Feel free to use and modify.
Updated 5/14/2017 to add sound via Pygame

Besides causing an LED on GPIO pin 17 to flash, the new version of morse.py can
play 1000 Hz tone files, one for dah (300 msec and one for dit (100 msec)

Make sure to pick up the sound files dit.wav and dah.wav
The tones were generated with Audacity. They are 1000 Hz.
The dit tone last for 100 msec and the dah tone for 300 msec.
Dit.wav and dah.wav must be placed in the same folder as morse.py

Further projects might be to use either a microphone or a light detector 

Various command line options exist. To see them, run morse.py
usage: morse.py ["message to be encoded"] [-ns] [-r NumberOfRepeats ] [-d}')
multiple word messages must be within quotes
-ns is the no sound option
-d cause verbose output to be printed
-r N causes a message to repeat N times

