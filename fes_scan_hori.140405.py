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


    print 'File prefix ='

    infolist=[]

# Counter channel
    cnt_ch1=0 #100605 IC  before Mirror
    cnt_ch2=3 #100605 PIN before Mirror

# FES scan setting
    scan_apert=0.05
    scan_another_apert=0.5
    scan_start=-1.5
    scan_end=2.0
    scan_step=0.05
    scan_time=0.2

# Height offset 140405 0.044mm
    height_offset=0.044

# FES hori scan
    prefix="%03d"%f.getNewIdx3()
    fes.scanH(prefix,scan_another_apert+height_offset,scan_apert,scan_start,scan_end,scan_step,cnt_ch1,cnt_ch2,scan_time)

# Save current axes information
    prefix="%03d"%f.getNewIdx3()
    ofile=prefix+"_axes.dat"
    axes.all(ofile)

    s.close()
    break
