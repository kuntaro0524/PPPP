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

    print 'File prefix ='

    infolist=[]

# Counter channel
    cnt_ch1=3
    cnt_ch2=0

# TCS full open
    tcs.setApert(3.0,3.0)

# TCS zero-aperture check
    prefix="%02d"%f.getNewIdx("scn")
    tcs.checkZeroV(prefix,0.5,-0.5,-0.05,cnt_ch1,cnt_ch2,0.2)

    prefix="%02d"%f.getNewIdx("scn")
    tcs.checkZeroH(prefix,0.5,-0.5,-0.05,cnt_ch1,cnt_ch2,0.2)

    s.close()
    break
