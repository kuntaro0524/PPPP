#!/bin/env python 
import sys
import socket
import time

# My library
from Received import *
from Organizer import *
from PeakFWHM import *
from ID import *
from TCS import *
from AxesInfo import *
from Dtheta import *
from ExSlit1 import *

host = '172.24.242.41'
port = 10101
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))

#


while True:
    print "Input index [example. 00, 01,...]:"
    data_index = int(raw_input())
 
# Constructer
    stmono=Organizer(s,"bl_32in","tc1_stmono_1","")
    tcs=TCS(s)
    id=ID(s)
    dtune=DthetaTune(s)
    ex2slit=ExSlit(s)
    axes=AxesInfo(s)

# Intensity monitor channels
    ch_pin=2
    ch_ic=1

#Energy
    e=12.398 # keV

# Initialize HW
    ex2slit.fullOpen()
    tcs.setApert(1.0,1.0)

# main 
# energy string
    en_str="%-8.3f"%float(e)

# Prefix setting
    prefix="%02d_mono_%skeV" % (data_index,en_str.strip())

# Storing axes information
    tmp=prefix+"_axes.dat"
    axes.all(tmp)

# Moving monochro 
    stmono.move(e,"kev")

# Moving ID
    id.moveE(e)

# Tuning dtheta1
    tcs.setApert(1.0,1.0)
    dtune.do(prefix,ch_pin,ch_ic)

# TCS scan
    tcs.scan(prefix,ch_pin,ch_ic)

# TCS zero check
    tcs.checkZeroV(prefix,1.0,0.03,-0.01,0.2,ch_pin)
    tcs.checkZeroH(prefix,1.0,0.03,-0.01,0.2,ch_pin)

# TCS zero check
    s.close()

    break
