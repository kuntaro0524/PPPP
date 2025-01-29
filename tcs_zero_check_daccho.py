#!/bin/env python 
import sys
import socket
import time

# My library
from Received import *
from Organizer import *
from ID import *
from Mono import *
from File import *
from TCS import *
from AxesInfo import *
from ExSlit1 import *
from ConfigFile import *

while True:
    host = '172.24.242.41'
    port = 10101
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host,port))

    # Initialization
    id=ID(s)
    mono=Mono(s)
    tcs=TCS(s)
    f=File("./")
    axes=AxesInfo(s)
    exs1=ExSlit1(s)
    conf=ConfigFile()

# Counter channel
    cnt_ch1=0
    cnt_ch2=3

    prefix="%03d"%f.getNewIdx3()

# If you require, please remove "#"
    #mono.scanDt1PeakConfig(prefix,"DTSCAN_NORMAL",tcs)

# check zero parameters
    start_apert=0.1
    end_apert=-0.1
    step=-0.005
    cnt_time=0.2

# TEST1
    start_apert=2.0
    step=-0.05

# TCS full open
    tcs.setApert(1.0,1.0)

# TCS zero-aperture check
    prefix="%03d"%f.getNewIdx3()
    tcs.checkZeroV(prefix,start_apert,end_apert,step,cnt_ch1,cnt_ch2,cnt_time)

    prefix="%03d"%f.getNewIdx3()
    tcs.checkZeroH(prefix,start_apert,end_apert,step,cnt_ch1,cnt_ch2,cnt_time)

    s.close()
    break
