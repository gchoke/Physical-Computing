#!/usr/bin/env python3
"""
#This program is intended to run on a raspberry pi.
#It converts a text message to morse code.
#It can be run from a terminal session or Idle
#Python 3 is assumed

#The program uses parallel lists letters, and codes to store the letters and
#morse code encryptions.

#The gpiozero module is used to create an instance of LED on GPIO port 17.
#It necessary to hook up an led with a current limiting resistor on that pin.
#Created by Greg Hoke on 5/12/2017 as an assignment for an RPi 
#Physical Computing Course. Feel free to use and modify.
#Updated 5/14/2017 to add sound via Pygame
#
#Make sure to pick up the sound files dit.wav and dah.wav
#The tones were generated with Audacity. They are 1000 Hz.
#The dit tone last for 100 msec and the dah tone for 300 msec.
#Dit.wav and dah.wav must be placed in the same folder as morse.py
#
#Further projects might be to use either a microphone or a light detector 
$to read interpret the morse code, formaing a closed loop communications system

"""
import pygame, sys
from gpiozero import LED
from time import sleep
from pygame.locals import *

led = LED(17)

di_time = 0.10 # sec
dah_time = 3*di_time
intra_char_time = 3*di_time
inter_word_time = 7*di_time

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


def is_integer(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

DEBUG = False
repeat = 1
message = "SOS."
message=".,,?!:'="
rflag = False 
#message = "Now is the time for all good men (and women) \
#           to come to the aid of their country"

SOUND = True  # sound can be suppressed with -ns option   
if len(sys.argv) > 1 :
    
    for i in range(len(sys.argv)) :
        if ( i == 0 ) : continue
        if (rflag ) :
            rflag = False
            continue
        if sys.argv[i] == "-d" :
            DEBUG = True
        if sys.argv[i] == "-r" and is_integer(sys.argv[i+1]) :
            repeat = int(sys.argv[i+1])
            rflag = True # kludge to avoid replacing message with the number
        elif (sys.argv[i] == '-h' ) :
            print ('usage: %s [\"message to be encoded\"] [-ns] \
[-r NumberOfRepeats ] -d')
            print ("multiple word messages must be within quotes")
            print ("-ns is the no sound option")
            print ("-d cause verbose output to be printed")
            print ("-r N causes a message to repeat N times")
            quit()
        elif (sys.argv[i] == '-ns' ) :
            SOUND = False
        else :
            if ( sys.argv[i][0] != '-' ) :
                message = sys.argv[i]
            
if ( SOUND ) :            
    pygame.init()
    SOUNDS = {}
    SOUNDS['dit'] = pygame.mixer.Sound('dit.wav')
    SOUNDS['dah'] = pygame.mixer.Sound('dah.wav')
    
message = message.upper()   # since morse code only handles upper case
print (message)
print ("repeating %d" % (repeat))
encrypted = []

for i in range(len(message) ) :
    if ( message[i] == ' ' ) :
        if ( DEBUG ) :
            print (message[i])
        encrypted.append(".......")
        continue
    for j in range(len(letters)) :
        if ( message[i] == letters[j] ) :
            break
        
    if ( j < len(letters) ) :
        if ( DEBUG ) :
            print (message[i], " = ", codes[j])
        encrypted.append(codes[j])
    else :
        print ("message character %s not found!" % (message[i]) )

if ( DEBUG ) :
    print("----------------------Decoding Test --------------------------")
for i in range(len(encrypted)) :
    for j in range(len(codes)) :
        if ( encrypted[i] == codes[j] ) :
            break
    if ( DEBUG ) :
        if ( j < len(codes) ) :
            print (encrypted[i], " = ", letters[j])
        else :
            print ("coded character %s not found!" % (encrypted[i]) )

count = repeat # in case you wish to repeat your message as in "SOS"
while count >= 1 : 
    for i in range(len(encrypted)) :
        
        if ( encrypted[i] == space ) :
            sleep(inter_word_time)
            continue
        
        sys.stdout.write(encrypted[i]) # suppress newlines
        sys.stdout.write(' ')
        sys.stdout.flush()
        
        
        for j in range(len(encrypted[i]) ) :
            
            if ( encrypted[i][j] == '.' ) :
                led.on()
                if ( SOUND ) :
                    SOUNDS['dit'].play()
                sleep(di_time)
                led.off()
                sleep(di_time)
            if ( encrypted[i][j] == '-' ) :
                #led.blink(dah_time,di_time,1)
                led.on()
                if ( SOUND ) :
                    SOUNDS['dah'].play()
                sleep(dah_time)
                led.off()
                sleep(di_time)

        sleep(intra_char_time)
    
    
    sleep(inter_word_time)

    count -= 1

print()
