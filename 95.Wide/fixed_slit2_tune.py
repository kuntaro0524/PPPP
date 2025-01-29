#!/bin/env python

import sys
import socket
import time
import datetime

# My library
from File import *
from ExSlit2 import *
from BM import *
from Capture import *
from Count import *
from Mono import *

host = '172.24.242.41'
port = 10101
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))

while True:

# block observation time[sec]
	block_time=3600
# Count time[sec]
	count_time=1.0

# Detector number
	pin3=3
	pin2=2
	ic=0
	step=20

	mono=Mono(s)
	bm=BM(s)
       	f=File("./")
	slit2=ExSlit2(s)
	cap=Capture()

# Devices
	for iloop in range(0,8):
		# BM off
		bm.set(-75000)

		# slit2 aperture -> narrow
		slit2.setSize(46,200)

		# Delta theta1 tune
        	prefix="%03d"%(f.getNewIdx3())
        	mono.scanDt1Peak(prefix,-95000,-90000,step,pin3,ic,0.2)

		# slit2 aperture -> Full open
		slit2.fullOpen()

		# File name
		filename="%s_fixed.scn"%(prefix)
		of=open(filename,"w")

		# Fixed point 
        	starttime=time.time()
		strtime=datetime.datetime.now()
        	of.write("#### %s\n"%strtime)
        	ttime=0

		counter=Count(s,pin3,ic)
        	while (ttime <= block_time ):
                	currtime=time.time()
                	ttime=currtime-starttime
                	ch1,ch2=counter.getCount(count_time)
                	of.write("12345  %8.3f %12d %12d\n" %(ttime,ch1,ch2))
			of.flush()

		strtime=datetime.datetime.now()
        	of.write("#### %s\n"%strtime)
        	of.close()

		# Insert BM
		bm.set(-500)
		time.sleep(3)
	
		# Capture
		idx=1
		path=os.path.abspath("./")
		imgfile="%s/%s.ppm"%(path,prefix)

        	cap.capture(imgfile)

		# Axes information 
		#j.tmpname="02_final_axes.dat"
		#axes.all(tmpname)

	break

s.close()
