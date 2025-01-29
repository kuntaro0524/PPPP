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
from ConfigFile import *

while True:
    host = '172.24.242.41'
    port = 10101
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host,port))

    # Initialization
    fes=FES(s)

# FES open
    vert=float(sys.argv[1])
    hori=float(sys.argv[2])

    if vert > 0.7 or hori > 0.7:
	print "DAME"
	sys.exit(1)

    fes.setApert(vert,hori)
    break
