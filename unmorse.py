#!/usr/bin/env python3

import sys

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
DEBUG = True

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

if len(sys.argv) != 2 :
    print ("usage: %s morse_coded_message" % (sys.argv[0]))
    quit()

coded = sys.argv[1]
print (coded)
print ("calling decrypt")
encrypted = coded.split(' ')
msg = decrypt(encrypted)
msg1 = ''.join(msg)
print (msg1)
