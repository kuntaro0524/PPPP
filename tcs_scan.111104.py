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

# TCS scan parameters
    scan_apert=0.05
    scan_another_apert=0.5
    scan_start=1.4
    scan_end=2.2
    scan_step=0.05
    scan_time=0.2

# Energy 
    energy=12.3984

# Energy change
    mono.changeE(energy)

# Gap 
    id.moveE(energy)

# TCS full open
    #tcs.setApert(3.0,3.0) ##101025 hashi

# Dtheta1 tune
    prefix="%03d"%f.getNewIdx3() ##101025 hashi
    mono.scanDt1PeakConfig(prefix,"DTSCAN_NORMAL",tcs)

# TCS vertical scan
    prefix="%03d"%f.getNewIdx3()
    prefix="%03d_tcs"%f.getNewIdx3()
    vcenter1,tmp=tcs.scanVrel(prefix,0.05,0.5,1.4,scan_step,cnt_ch1,cnt_ch2,scan_time)
    hcenter1,tmp=tcs.scanHrel(prefix,0.50,0.05,1.4,scan_step,cnt_ch1,cnt_ch2,scan_time)
    #vcenter1,tmp=tcs.scanVrel(prefix,0.40,0.5,1.4,scan_step,cnt_ch1,cnt_ch2,scan_time)
    #hcenter1,tmp=tcs.scanHrel(prefix,0.50,0.40,1.4,scan_step,cnt_ch1,cnt_ch2,scan_time)

    #tcs.scanBoth(prefix,scan_apert,scan_another_apert,scan_start,scan_end,scan_step,cnt_ch1,cnt_ch2,scan_time)
    #tcs.setApert(1.0,1.0)

# Save current axes information
    s.close()
    break
