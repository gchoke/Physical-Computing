#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time

__author__ = 'Gus (Adapted from Adafruit)'
__license__ = "GPL"
__maintainer__ = "pimylifeup.com"

#GPIO.setmode(GPIO.BOARD)
GPIO.setmode(GPIO.BCM)

#define the pin that goes to the circuit
pin_to_circuit = 18

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
try:
    # Main loop
    i = 0
    #while True:
    while i < 100 :
        print (rc_time(pin_to_circuit))
        i += 1
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
