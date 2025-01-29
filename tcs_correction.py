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

    # Initialization
    tcs=TCS(s)

    # Get current information
    outfile=open("tcs_info.dat","w")

    apert= tcs.getApert()
    position= tcs.getPosition()

    outfile.write("APERT: %s %s\n"%(apert[0],apert[1]))
    outfile.write("POSI : %s %s\n"%(position[0],position[1]))

    s.close()
    break
