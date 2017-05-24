#!/usr/bin/env python3

from gpiozero import LightSensor

ldr = LightSensor(18)

while True:
        ldr.wait_for_light()
        print(" light is on")
        ldr.wait_for_dark()
        print("light is off")
