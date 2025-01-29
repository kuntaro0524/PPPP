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
    id=ID(s)
    mono=Mono(s)
    fes=FES(s)
    tcs=TCS(s)
    f=File("./")
    axes=AxesInfo(s)

# Counter channel
    cnt_ch1=0 #0
    cnt_ch2=3 #1

# TCS default position
    tcsv=-0.5190
    tcsh=-0.5125

    tcs.setPosition(tcsv,tcsh)

# TCS vertical scan
# Horizontal blade check
    #tcs.setApert(0.5,0.05)
    #tcs.setApert(0.05,0.5)
    for x in arange(-1.0,0.0,0.05):
        nprint "Current X: %8.2f"%x
        ntcs.setPosition(tcsv,x)
        ntime.sleep(2.0)

    tcs.setPosition(tcsv,tcsh)
# Save current axes information
    s.close()
    break
