#!/bin/env python 
import sys
import socket
import time

# My library
from Received import *
from Organizer import *
from ID import *
from Mono import *
from FES import *
from File import *
from TCS import *
from AxesInfo import *

while True:
    host = '172.24.242.41'
    port = 10101
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host,port))

    if len(sys.argv)!=3:
       print "Usage: PROGRAM V_APERT H_APERT"
       sys.exit()

    # Initialization
    tcs=TCS(s)

    # TCS full open
    # vertical -> horizontal
    tcs.setApert(float(sys.argv[1]),float(sys.argv[2]))

    s.close()
    break
