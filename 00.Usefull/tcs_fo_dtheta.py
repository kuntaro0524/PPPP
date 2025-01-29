#!/bin/env python 
import sys
import socket
import time
import datetime

# My library
from Received import *
from Organizer import *
from Dtheta import *
from FES import *
from ID import *
from TCS import *
from AxesInfo import *
from ExSlit1 import *

host = '172.24.242.41'
port = 10101
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))

while True:

# Energy list
    en_list=[10,12.398,14,15,16,17,18,19,20]

# Slit size list
    tcs_open_aperture=[1.0,1.0]

# Detector number
    cnt_ch1=0
    cnt_ch2=1

# Devices
    id=ID(s)
    dt=DthetaTune(s)
    tcs=TCS(s)
    axes=AxesInfo(s)
    slit2=ExSlit1(s,cnt_ch1)

    index=0
    sizei=0

    for en in en_list :
	# index
	index+=1
	# file prefix
	prefix="%02d"%index

	#moving the fisrt position
    	id.moveE(en)
    	stmono.move(en,"kev")

	# PREFIX
	prefix="%s_%skev"%(prefix,en)

	sizei=0
	sizei+=1
	prefix_tmp="%s_%02d" % (prefix,sizei)


	##  dtheta1 tune @ TCS 5.0mm x 5.0mm
	tcs.setApert(tcs_open_aperture[0],tcs_open_aperture[1])
    	dt.do(prefix_tmp,cnt_ch1,cnt_ch2)

	# TCS scan
	tcs.scan(prefix_tmp,cnt_ch1,cnt_ch2)

	# ExSlit1
	slit2.scanBoth(prefix_tmp)

	# Axes information 
	tmpname="%s_axes.dat"%prefix
	axes.all(tmpname)

    s.close()

    break
