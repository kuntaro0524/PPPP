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
    cnt_ch1=0 #3
    cnt_ch2=3 #0

# FES 0 check parameter
    start_apert=0.5
    end_apert=-0.1
    step=-0.05
    cnt_time=0.2

# Dtheta1 tune range
    scan_dt1_start=-96500
    scan_dt1_end=-92500
    scan_dt1_step=20
    scan_dt1_time=0.2

# Energy change to 23.2keV
    mono.changeE(23.2)
# Gap full open
    id.move(45.0) # Full open

# TCS full open
    fes.setApert(0.3,0.3)
    tcs.setApert(3.0,3.0)

# Dtheta1 tune
    prefix="%03d"%f.getNewIdx3()
    mono.scanDt1(prefix,scan_dt1_start,scan_dt1_end,scan_dt1_step,cnt_ch1,cnt_ch2,scan_dt1_time)

# Save current axes information
    prefix="%03d"%f.getNewIdx3()
    ofile=prefix+"_axes.dat"
    axes.all(ofile)

# FES zero-aperture check
    prefix="%03d"%f.getNewIdx3()
    fes.checkZeroV(prefix,start_apert,end_apert,step,cnt_ch1,cnt_ch2,cnt_time)

    prefix="%03d"%f.getNewIdx3()
    fes.checkZeroH(prefix,start_apert,end_apert,step,cnt_ch1,cnt_ch2,cnt_time)

    s.close()
    break
