#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time

__author__ = 'Greg Hoke (Adapted from Gus (of pimylifeup.com) and Adafruit)'
__license__ = "GPL"
__maintainer__ = "Greg"


##########################################################################
# ldrDetect.py attempt to detect morse code from a flashing LED
# It is  shamelessly modified version of ldrTest.py obtained from
# https://pimylifeup.com/raspberry-pi-light-sensor
# The morse code message is converted to letters when the
# user hits ctrl-C. Run this command in one window while
# morse.py is sending a message.
# With the DEBUG flag set to True a lot messages get printed
# out which adversely affects detection accuracy.
# Use DEBUG with caution, although it is interesting to see
# the timing information. Those print statements take a lot of time to run...
#########################################################################

DEBUG = False
#define the pin that goes to the circuit
pin_to_circuit = 18

"""

This project detects Morse Code with an LDR looking at a flashing LED.
Another python script named morse.py flashes the LED, so you need to run
this detector script at the same time as morse.py.
The minimum dit time and the time between bits is only 0.1 seconds
The time for a dah is 3 times the dit time, or 0.3 seconds.

Instructions:
1) Set up an LED with a 220 ohm resistor and LDR with a 0.47 uF capacitor.
2) The LDR is a light sensor that has about 150 ohm when lit
   and 2000 ohm when dark. It charges the capacitor and the RPi
   GPIO port detects when the capacitor voltage goes high.
   A dark LDR takes longer to charge because of the higher LDR
   resistance. Connect one leg of the LDR to RPi 3.3 V. The other
   leg gets connected to the capacitor. The other end of the capacitor is
   connected to ground. (Note that electrolytic capaciotrs are bipolar with
   a "minus" showing on the capacitor body. This is the end that connects to
   ground.) The junction point between the LDR and capacitor is connnected to
   the RPi GPIO port 18. (Change pin_to_circuit if you decide to use a
   differnet GPIO port.)
3) If you want to experiment with morse code detection, the morse.py script
   flashes the LED on GPIO port 23 while ldrDetect.py "listens" via the LDR
   on GPIO 18.
4) To cloak the LED and LDR I used a tube made out of a CAT \5 ethernet cable
   cover. It was just the right size to allow the LED to be on one end with LDR on the
   other. This way i could get similar results day or night. I got varying
   results with different LEDs. Choose a clear bright LED for best results.
   The LDR came from a company called SUNKEE model number X001C9BA9.
5) To test the morse code detection run ldrDetect.py at the same time as
   morse.py converts english text to morse code and flashes the LED. (It also
   plays 1000 Hz tones for the dits and dahs which you can suppress by
   running with the -ns option or disconnecting the RPi speaker.)
6) The detected message will appear on the screen when you do a keyboard
   interrupt of ldrDetect.py. The message should be intelligible but with some
   errors.
   Example session:
    morse.py "the quick red fox jumped over the sleeping yellow dog."
THE QUICK RED FOX JUMPED OVER THE SLEEPING YELLOW DOG.
repeating 1
- .... . --.- ..- .. -.-. -.- .-. . -.. ..-. --- -..- .--- ..- -- .--. . -.. --- ...- . .-. - .... . ... .-.. . . .--. .. -. --. -.-- . .-.. .-.. --- .-- -.. --- --. .-.-.- 
   
  ldrDetect.py output:
  (The " ....... " key is inserted to indicate spaces.)
  detected morse Message = " ....... - .... - ....... --.- ..- .. -.-. -.- ....... .-. . --. ....... -.-. --- -..- ....... .--- ..- -- .--. . --. ....... --- ..-- . .-. ....... - .... . ....... ... .-.. . . .--. .. -. --. ....... -.-- . --.. .-.. --- --- ....... -.. --- --- .-.-.-"
 THT QUICK REG COX JUMPEG OER THE SLEEPING YEZLOO DOO.

The detector has to be quick to interpret the flashes and the pauses.
There are different pauses for bit separation, character breaks, and word breaks.
Attempts to use GPIOZERO LightSensor seemed hopeless because it missed
too many pauses and bits.
This script entitle ldrDetect.py is a modification of the ldrTest.py script
which uses a RPi.GPIO library instead of GPIOZERO.

Consequently I am using another method to detect
experimental results using ldrTest.py | mstat
Note that results varied with capacitor and LED

This result was with a 0.47uF mylar capacitor (aka, green "chicklet" marked 474J) cap
and a bright, clear LED. A red LED resulted in very poor results
where max(On) < min(Off) in some cases.

The following table is from ldrTest.py, also in this repository. The units are
in msec. I wrote a C command called mstat.c to generate the statistics.
Compile on the raspberry pi with
gcc -o mstat mstat.c -lm
ldrTest.py automatically stops after 100 measurements. In one case the LED is on. In the
second the LED is off. Use ldrTest.py | mstat to test your own system. You
want the maximum "On" detection time to be much less than the minimum
"Off" detection time. Recall that the charging times are related tothe variable
resistance of the LDR when lit (150 ohms) and when dark (2100 ohoms)

The LED and LDR faced each other inside a tube to block ambient light.

Averging on(max) and off(Min) we find: (10.8519 + 26.6786) / 2 = 18.765
So 18 msec (0.018 sec) is a good threshold to distinguish LED on and LED off.
This is less than 20% of the 100 msec dit time, so it is acceptable.

            N      Min     Med      Max      Avg      Var      SD       CV%
Light on:  100  10.5698  10.5989  10.8519  10.6135  1.14033  1.06786  10.0613
Light off: 100  26.6786  26.8087  29.5076  27.21    7.93895  2.81761  10.3551
"""


letters=[" ","A","B","C","D","E","F","G","H","I",\
         "J","K","L","M","N","O","P","Q","R","S",\
         "T","U","V","W","X","Y","Z",\
         "1","2","3","4","5","6","7","8","9",\
         '.', ",", "?", "!", ":", '\"','\'',"="]
codes=[".......", ".-","-...","-.-.","-..",".","..-.","--.","....","..",\
      ".---","-.-",".-..","--","-.","---",".--.","--.-",".-.","...",\
      "-","..-","...-",".--","-..-","-.--","--..",
      ".----","..---","...--","....-",".....","-....","--...","---..","----.",
      ".-.-.-","--..--","..--..","..--.","---...",".-..-.",".----.","-...-"]

space = "......."


def decrypt(encrypted) :
    message = []
    for i in range(len(encrypted)) :
        for j in range(len(codes)) :
            if ( encrypted[i] == codes[j] ) :
                message.append(letters[j])
                break
        if ( DEBUG ) :
            if ( j < len(codes) ) :
                print (encrypted[i], " = ", letters[j])
            else : 
                print ("coded character %s not %found!" % (encrypted[i]))
    return message

#GPIO.setmode(GPIO.BOARD)
GPIO.setmode(GPIO.BCM)



def rc_time (pin_to_circuit):
    start = time.time()
    count = 0
  
    #Output on the pin for 
    GPIO.setup(pin_to_circuit, GPIO.OUT)
    GPIO.output(pin_to_circuit, GPIO.LOW)
    time.sleep(0.01)

    #Change the pin back to input
    GPIO.setup(pin_to_circuit, GPIO.IN)
  
    #Count until the pin goes high
    while (GPIO.input(pin_to_circuit) == GPIO.LOW):
        count += 1

    #return count
    return 1000*(time.time() - start) # msec

#Catch when script is interupted, cleanup correctly

LdrThreshold = 18 # scaled down to msec
UNKNOWN = 0
LIGHT = 1
DARK = 2
state = UNKNOWN
toneStart = time.time()
silStart = time.time()
toneDitDahThreshold = 0.15
silSymbolCharThreshold = 0.15
silCharWordThreshold = 0.5
morseMsg = ""

startUp = True # fix bug of saving a spurios dit 
try:
    # Main loop
    while True:
        detectTime = rc_time(pin_to_circuit)
        
        if ( detectTime < LdrThreshold ) :
            
            if ( state != LIGHT ) :
                if ( DEBUG ) :
                    print("detectTime = %g, LdrThreshold = %g" % \
                          (detectTime, LdrThreshold))
                state = LIGHT
                if ( DEBUG ) :
                    print("Light turned on")
                toneStart = time.time()
                silDuration = time.time() - silStart
                
                if ( silDuration > silSymbolCharThreshold and \
                     silDuration < silCharWordThreshold) :
                    if ( DEBUG ) :
                        print ("silDuration = %g: character" % (silDuration))
                    morseMsg += ' ' # add a space for a character boundary
                elif (silDuration > silCharWordThreshold ) :
                    if ( DEBUG ) :
                        print ("silDuration = %g: word" % (silDuration))
                    morseMsg += " ....... " # word boundary
                else :
                    if ( DEBUG ) :
                        print ("silDuration = %g: UNCLASSIFIED" % (silDuration))  
        else :
            if ( state != DARK ) :
                if ( DEBUG ) :
                    print("detectTime = %g, LdrThreshold = %g" % \
                      (detectTime, LdrThreshold))
                    print("Light turned off")
                state = DARK
                silStart = time.time()
                toneDuration = time.time() - toneStart
                
                if ( startUp == True ):
                    startUp = False
                    continue
                if ( toneDuration < toneDitDahThreshold ) :
                    morseMsg += '.' # a dit
                    if ( DEBUG ) :
                        print("toneDuration = %g: dit" % (toneDuration))
                else :
                    morseMsg += '-' # a dah
                    if ( DEBUG ) :
                        print("toneDuration = %g: dah" % (toneDuration))
    
except KeyboardInterrupt:
    print ("detected morse Message = \"%s\"" % (morseMsg))
    encrypted = morseMsg.split(' ')  # convert text string to list
    msg = decrypt(encrypted)    # returns a list
    print (''.join(msg) )       # our best guess
    pass
finally:
    GPIO.cleanup()
