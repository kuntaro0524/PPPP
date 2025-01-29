#!/bin/env python 
import sys
import socket
import datetime

# My library
from Received import *
from Motor import *

host = '172.24.242.41'
port = 10101
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))

#

while True:
    print 'File prefix ='
    prefix = raw_input()
 
    infolist=[]

# Energy change to 23.2keV
# Gap full open
# Move Mono
# Dtheta1 tune

    s.close()

    break
