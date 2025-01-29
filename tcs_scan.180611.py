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
    scan_apert=0.10
    scan_another_apert=0.50
    scan_start=-0.5
    scan_end=0.5
    scan_step=0.05
    scan_time=0.1

# TCS scan
    prefix="%03d"%f.getNewIdx3()
    tcs.scanH(prefix,scan_another_apert,scan_apert,scan_start,scan_end,scan_step,cnt_ch1,cnt_ch2,scan_time)

    s.close()
    break
