# Reuirments 
 
# WIP - 1. Write a program which will parse this data. It should allow the user to specify a serial port to open on the command line. Note, that if you choose C++, you can't use any C++11 features except 'auto'.
# DONE - 2. The data should be converted into JSON format, with an extra boolean field called 'VALID' which will signify that the TOTAL field is correct.
# NA ( will not fit in demo) 3. On each 10 seconds system time boundary, eg 2:00:00pm, 2:00:10pm, 2:00:20pm the program should print the latest JSON data to stdout.
#4.DONE The program should run on Ubuntu 16.04 and use a makefile to build.
#5. DONE You can use any libraries you wish to complete this task, please specify any packages which need to be installed to allow your program to build under 16.04.
#6. DONE Place the code on a publicly available git server and send URL details.

import os, pty, serial
import json
master, slave = pty.openpty()

# Create a communication port and listen on it
s_name = os.ttyname(slave)
print("We are listening now Please connect to device:", s_name)

ser = serial.Serial(s_name)

# To read from the device
os.read(master,1000)

while True:
    rcvd = os.read(master,1000)
    l = rcvd.strip().replace(':', '  ').split()
    l.pop()
    l.pop(0)
    j = {}

    total = 0
    expected_total = 0
    for i in range(0,len(l)-2, 3):
        try:
            key = l[i]
            value = float(l[i+1])
            if not key == 'TOTAL':
                total+= value
            else:
                expected_total = value

            j [key] = value
            
        except Exception as ex:
            print("Invalid data recieved")
            print(ex)
            continue

    j['Valid'] = total== expected_total

    print(json.dumps(j, sort_keys=True, indent=4))
