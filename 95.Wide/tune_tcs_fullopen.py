#!/bin/env python 
import sys
import socket
import time

# My library
from ID import *
from Mono import *
from TCS import *
from File import *

host = '172.24.242.41'
port = 10101
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))

while True:

    # Initialization
    id=ID(s)
    mono=Mono(s)
    f=File("./")
    tcs=TCS(s)

    infolist=[]

# Counter channel
    cnt_ch1=3
    cnt_ch2=0

# Energy change
    mono.changeE(12.398)
# Gap full open
    id.moveE(12.398)
# TCS full open
    tcs.setApert(3.0,3.0)
# Dtheta1 tune
    prefix="%02d"%f.getNewIdx("scn")
    mono.scanDt1(prefix,-92000,-89500,20,cnt_ch1,cnt_ch2,0.2)

# TCS 0.1mm square
    tcs.setApert(0.1,0.1)

    s.close()

    break
