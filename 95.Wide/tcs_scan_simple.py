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

# Dtheta1 tune
    scan_dt1_start=-95000 ## b4 100629 -88000
    scan_dt1_end=-90000   ## b4 100629 -82000
    scan_dt1_step=20
    scan_dt1_time=0.2

# TCS full open
#   tcs.setApert(3.0,3.0)
# Dtheta1 tune
#   prefix="%03d"%f.getNewIdx3()                                                                 #hashi 100615
#    mono.scanDt1(prefix,scan_dt1_start,scan_dt1_end,scan_dt1_step,cnt_ch1,cnt_ch2,scan_dt1_time) #hashi 100615
#   mono.scanDt1Peak(prefix,scan_dt1_start,scan_dt1_end,scan_dt1_step,cnt_ch1,cnt_ch2,scan_dt1_time) #hashi 100615
# TCS scan
    prefix="%03d"%f.getNewIdx3()
    tcs.scanBoth(prefix,scan_apert,scan_another_apert,scan_start,scan_end,scan_step,cnt_ch1,cnt_ch2,scan_time)
    tcs.setApert(3.0,3.0)

# Save current axes information
    prefix="%03d"%f.getNewIdx3()
    ofile=prefix+"_axes.dat"
    axes.all(ofile)

    s.close()
    break
