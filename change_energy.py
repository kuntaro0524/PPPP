#!/bin/env python 
import sys
import socket
import time

# My library
from ID import *
from Mono import *

host = '172.24.242.41'
port = 10101
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))

while True:

    # Initialization
    id=ID(s)
    mono=Mono(s)

    energy=float(sys.argv[1])
# Energy change
    mono.changeE(energy)
    print "Monochromator moved\n"
# Gap 
    id.moveE(energy)
    print "ID moved\n"
    s.close()

    break
