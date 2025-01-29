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
from ConfigFile import *

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
    conf=ConfigFile()

    infolist=[]

# Counter channel
    cnt_ch1=0 # IC  before Mirror
    cnt_ch2=3 # PIN before Mirror

# FES offset
    height_offset=0.044

# FES scan setting
    scan_apert=0.05
    scan_another_apert=0.5
    scan_start=-1.5
    scan_end=2.0
    scan_step=0.05
    scan_time=0.2

# FES open
    fes.setApert(0.3,0.3)
# TCS full open
    tcs.setApert(3.0,3.0)

# FES vertical scan
    prefix="%03d"%f.getNewIdx3()
    scan_apert+=height_offset
    fes.scanV(prefix,scan_apert,scan_another_apert,scan_start,scan_end,scan_step,cnt_ch1,cnt_ch2,scan_time)

    s.close()
    break
