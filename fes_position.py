#!/bin/env python 
import sys
import socket
import time

# My library
from FES import *

while True:
    host = '172.24.242.41'
    port = 10101
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host,port))

    # Initialization
    fes=FES(s)
	
# Acquiring position
    if len(sys.argv)<3 :
	print "PROGRAM FES_V[mm] FES_H[mm]"
	sys.exit()
    else:
	vert=float(sys.argv[1])
	hori=float(sys.argv[2])
	fes.setPosition(vert,hori)
	break
