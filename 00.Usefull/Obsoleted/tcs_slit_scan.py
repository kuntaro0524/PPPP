#!/bin/env python 
import sys
import socket
import time

# My library
from Received import *
from Organizer import *
from TCS import *

host = '172.24.242.41'
port = 10101
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))

#

while True:
    print time.clock()
    print 'File prefix ='
    prefix = raw_input()

    tcs=TCS(s)
    tcs.scan(prefix,1,2)

    s.close()

    break
