#!/bin/env python 
import sys
import socket
import time
import datetime

# My library
from Mono import *
from FES import *
from ID import *
from TCS import *
from ExSlit1 import *
from AxesInfo import *
from File import *
from FixedPoint import  *
from Att import *

host = '172.24.242.41'
port = 10101
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))

while True:

# Conditions
    en_list=[8.5,12.398,18.0]

# Detector number
    pin3=3
    ic=0

# Devices
    id=ID(s)
    mono=Mono(s)
    tcs=TCS(s)
    axes=AxesInfo(s)
    f=File("./")
    fixedp=FixedPoint(s)
    att=Att(s)

    index=0
    sizei=0

    # Log file
    logf=open("fixed_point.scn","w")

    for en in en_list :
	# Axes information 
	prefix="%03d"%f.getNewIdx3()
	enstr="%fkev"%en

	# Changing Energy
	if en==8.5:
		id.move(7.62)
	else:
    		id.moveE(en)

    	mono.changeE(en)

	# TCS aperture 0.1x0.1mm
	tcs.setApert(0.1,0.1)

	# Fixed point scan for 4 hour (See test.conf)
	# 20100703 - Fixed point scan for 4 hour x 3 times for each energy (See test.conf)
	str=fixedp.doMonitor(prefix)
	logf.write(str)
	logf.flush()

    s.close()

    break
