#!/bin/env python 
import sys
import socket
import time

# My library
from Received import *
from Organizer import *
from TCS import *

host = '172.24.242.41'
port = 10101
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))

#

while True:
    print time.clock()
    print 'File prefix ='
    prefix = raw_input()

    tcs=TCS(s)
    prefix="test"

    scan_height=0.05
    scan_width=0.50
    start=-1
    end=1
    step=0.05
    time=0.2
    cnt_ch1=0
    cnt_ch2=1

    tcs.scanV(prefix,scan_width,scan_height,start,end,step,cnt_ch1,cnt_ch2,time)

    scan_height=0.50
    scan_width=0.05

    tcs.scanH(prefix,scan_width,scan_height,start,end,step,cnt_ch1,cnt_ch2,time)

    s.close()

    break
