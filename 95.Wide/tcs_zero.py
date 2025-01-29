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
    cnt_ch1=3
    cnt_ch2=0

# check zero parameters
    start_apert=0.5
    end_apert=-0.1
    step=-0.01
    cnt_time=0.2

# TCS full open
    tcs.setApert(3.0,3.0)

# TCS zero-aperture check
    prefix="%03d"%f.getNewIdx3()
    tcs.checkZeroV(prefix,start_apert,end_apert,step,cnt_ch1,cnt_ch2,cnt_time)

    prefix="%03d"%f.getNewIdx3()
    tcs.checkZeroH(prefix,start_apert,end_apert,step,cnt_ch1,cnt_ch2,cnt_time)

    s.close()
    break
