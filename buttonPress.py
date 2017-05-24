#!/usr/bin/env python3

#################################################
#
# connect button between ground and GPIO pin 4
# connect the led anode (long leg) to GPIO pin 23 
# the cathode connect to a 320 ohom resister 
# The other side of the resitor goes to ground
#
#################################################

from gpiozero import Button, LED
btn = Button(4)
led = LED(23)

while True:
    btn.wait_for_press()
    print("You pressed me!")
    led.on()
    btn.wait_for_release()
    print("You released me!")
    led.off()
