#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import MFRC522
import signal

continue_reading = True

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()
    exit(0)

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# Welcome message
print "Welcome to the MFRC522 data write example"
print "Press Ctrl-C to stop."

# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:
    
    # Scan for cards    
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # If a card is found
    if status == MIFAREReader.MI_OK:
        print "Card detected"
    
    # Get the UID of the card
    (status,uid) = MIFAREReader.MFRC522_Anticoll()

    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:

        # Print UID
        print "Card read UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3])
    
        # This is the default key for authentication
        key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
        
        # Select the scanned tag
        MIFAREReader.MFRC522_SelectTag(uid)

        # Authenticate
        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)
        print "\n"

        # Check if authenticated
        if status == MIFAREReader.MI_OK:

            # Variable for the data to write
            data = []
            for x in range(0, 16):
                data.append(0)

            #sector_id = int(raw_input("Which sector would you like to write to? (Enter integer 1 through 8)\n"))
            print "Sector " + str(8) + " looked like this:"
            # Read desired block
            MIFAREReader.MFRC522_Read(8)
            print "\n"

            print "Please enter one 32-bit integer you would like to store."
            input = int(raw_input("Value: "))

            value = hex(input)[2:].zfill(8)
            for index in range(0, 8):
                data[index] = int(value[index], 16)

            #value = bin(input)[2:].zfill(16)
            #for index in range(0, 16):
            #    data[index] = int(value[index])

            # Write the data
            MIFAREReader.MFRC522_Write(8, data)
            print "\n"

            print "It now looks like this:"
            # Check to see if it was written
            MIFAREReader.MFRC522_Read(8)
            print "\n"

            # data = []
            # # Fill the data with 0x00
            # for x in range(0,16):
            #     data.append(0x00)

            # print "Now we fill it with 0x00:"
            # MIFAREReader.MFRC522_Write(8, data)
            # print "\n"

            # print "It is now empty:"
            # # Check to see if it was written
            # MIFAREReader.MFRC522_Read(8)
            # print "\n"

            # Stop
            MIFAREReader.MFRC522_StopCrypto1()

            # Make sure to stop reading for cards
            continue_reading = False
            print "Exiting Successfully. See you next time!"
        else:
            print "Authentication error"
