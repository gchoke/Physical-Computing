"""
This program is intended to run on a raspberry pi.
It converts a text message to morse code.

The program uses parallel lists letters, and codes to store the letters and
morse code encryptions.

The gpiozero module is used to create an instance of LED on GPIO port 17.
It necessary to hook up an led with a current limiting resistor on that pin.
Created by Greg Hoke on 5/12/2017 as an assignment for an RPi Physical Computing
Course. Feel free to modify and use.
"""
import sys
from gpiozero import LED
from time import sleep

led = LED(17)

di_time = 0.15 # sec
dah_time = 3*di_time
intra_char_time = 3*di_time
inter_word_time = 7*di_time

DEBUG = False

letters=[" ","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","1","2","3","4","5","6","7","8","9",""",".",",","?","!",""",":","'","="]
codes=[".......", ".-","-...","-.-.","-..",".","..-.","--.","....","..",".---","-.-",".-..","--","-.","---",".--.","--.-",".-.","...","-","..-","...-",".--","-..-","-.--","--..",".----","..---","...--","....-",".....","-....","--...","---..","----.",".-.-.-","--..--","..--..","..--.","---...",".-..-.",".----.","-...-"]
space = "......."
#message = "SOS"
message = "My name is Greg"
message = message.upper()   # since morse code only handles upper case
print (message)
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

for i in range(len(encrypted)) :
    for j in range(len(codes)) :
        if ( encrypted[i] == codes[j] ) :
            break
    if ( DEBUG ) :
        if ( j < len(codes) ) :
            print (letters[j], " = ", encrypted[i])
        else :
            print ("coded character %s not found!" % (encrypted[i]) )

count = 1 # in case you wish to repeat your message as in "SOS"
while count <= 1 : 
    for i in range(len(encrypted)) :
        
        if ( encrypted[i] == space ) :
            sleep(inter_word_time)
            continue
        
        sys.stdout.write(encrypted[i]) # suppress newlines
        sys.stdout.write(' ')
        
        
        for j in range(len(encrypted[i]) ) :
            
            if ( encrypted[i][j] == '.' ) :
                led.on()
                sleep(di_time)
                led.off()
                sleep(di_time)
            if ( encrypted[i][j] == '-' ) :
                #led.blink(dah_time,di_time,1)
                led.on()
                sleep(dah_time)
                led.off()
                sleep(di_time)

        sleep(intra_char_time)
    print
    count += 1
    sleep(inter_word_time)
