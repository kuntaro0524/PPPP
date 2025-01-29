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
    tcs=TCS(s)
    f=File("./")
    axes=AxesInfo(s)

# Counter channel
    cnt_ch1=0 #0
    cnt_ch2=3 #1

# TCS scan parameters
    scan_apert=0.37
    scan_another_apert=0.5
    scan_step=0.05
    scan_time=0.2

# TCS vertical scan
    prefix="%03d"%f.getNewIdx3()
    prefix="%03d_tcs"%f.getNewIdx3()
    #hcenter1,tmp=tcs.scanHrel(prefix,0.50,scan_apert,3.0,scan_step,cnt_ch1,cnt_ch2,scan_time)
    vcenter1,tmp=tcs.scanVrel(prefix,scan_apert,0.50,1.0,scan_step,cnt_ch1,cnt_ch2,scan_time)

    #print "Hcenter,Vcenter"
    #print hcenter1,vcenter1

# Save current axes information
    s.close()
    break
