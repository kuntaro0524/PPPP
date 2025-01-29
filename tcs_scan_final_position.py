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
    cnt_ch1=0
    cnt_ch2=3

# TCS scan parameters
    scan_apert=0.05
    scan_another_apert=0.5
    scan_start=-1.0
    scan_end=1.0
    scan_step=0.05
    scan_time=0.2

# TCS scan
    prefix="%03d"%f.getNewIdx3()
    # TCS vertical & horizontal scan x 1times
    prefix="%03d_tcs"%f.getNewIdx3()

    #vcenter1,tmp=tcs.scanV(prefix,0.05,0.5,0.7,2.7,scan_step,cnt_ch2,cnt_ch1,scan_time)
    #hcenter1,tmp=tcs.scanH(prefix,0.50,0.05,-1.2,0.80,scan_step,cnt_ch2,cnt_ch1,scan_time)
    tcs.scanBoth(prefix,scan_apert,scan_another_apert,scan_start,scan_end,scan_step,cnt_ch1,cnt_ch2,scan_time)

    tcs.setApert(0.1,0.1)

# Save current axes information
    prefix="%03d"%f.getNewIdx3()
    ofile=prefix+"_axes.dat"
    axes.all(ofile)

    s.close()
    break
