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
    cnt_ch1=3 #0
    cnt_ch2=0 #1

# TCS scan parameters
    scan_apert=0.05
    scan_another_apert=0.5
    scan_start=-0.5
    scan_end=1.5
    scan_step=0.05
    scan_time=0.2

# Energy 
    energy=12.3984

# Energy change
    mono.changeE(energy)

# Dtheta1 tune
    scan_dt1_start=-99000
    scan_dt1_end=-95000
    scan_dt1_step=20
    scan_dt1_time=0.2

# Gap 
    id.moveE(energy)

# TCS full open
    tcs.setApert(3.0,3.0)

# Dtheta1 tune
    prefix="%03d"%f.getNewIdx3()
    mono.scanDt1(prefix,scan_dt1_start,scan_dt1_end,scan_dt1_step,cnt_ch1,cnt_ch2,scan_dt1_time)

# FES vertical scan
    prefix="%03d"%f.getNewIdx3()
    tcs.scanBoth(prefix,scan_apert,scan_another_apert,scan_start,scan_end,scan_step,cnt_ch1,cnt_ch2,scan_time)
    tcs.setApert(3.0,3.0)

# Save current axes information
    prefix="%03d"%f.getNewIdx3()
    ofile=prefix+"_axes.dat"
    axes.all(ofile)

    s.close()
    break
