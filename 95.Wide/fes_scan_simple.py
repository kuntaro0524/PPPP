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

    print 'File prefix ='

    infolist=[]

# Counter channel
    cnt_ch1=0 #100605 IC  before Mirror
    cnt_ch2=3 #100605 PIN before Mirror

# FES scan setting
    scan_apert=0.05
    scan_another_apert=0.5
    scan_start=-1.5
    scan_end=1.5
    scan_step=0.05
    scan_time=0.2

# Energy change to 23.2keV
    mono.changeE(23.2)
# Gap full open
    id.move(45.0) # Full open

# FES open
    fes.setApert(0.3,0.3)

# TCS full open
    tcs.setApert(3.0,3.0)

# FES vertical scan
    prefix="%03d"%f.getNewIdx3()
    fes.scanBoth(prefix,scan_apert,scan_another_apert,scan_start,scan_end,scan_step,cnt_ch1,cnt_ch2,scan_time)

# Save current axes information
    prefix="%03d"%f.getNewIdx3()
    ofile=prefix+"_axes.dat"
    axes.all(ofile)

    s.close()
    break
