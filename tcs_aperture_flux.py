#!/bin/env python 
import sys
import socket
import time
import math
from pylab import *

# My library
from TCS import *
from Count import *
from ExSlit1 import *
from Shutter import *

while True:
	host = '172.24.242.41'
	port = 10101
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host,port))

##	Device definition
	tcs=TCS(s)
	f=File("./")
	exs1=ExSlit1(s)
	shutter=Shutter(s)

	tcs_list=[(0.1,0.1,0.2),(0.5,0.5,1.0),(1.0,1.0,1.0)]

## 	Log file
	logf=open("flux.log","w")

##	Counter channel
	cnt_ch1=3
	cnt_ch2=0

	exs1.openV()
	shutter.open()
	for tcs_param in tcs_list:
		# TCS aparture
		tcsv=float(tcs_param[0])
		tcsh=float(tcs_param[1])
		gstep=float(tcs_param[2])
	
		# TCS set aperture
		tcs.setApert(tcsv,tcsh)
	
		# TCS str
		tcsstr="%4.3fx%4.3f"%(tcsv,tcsh)

		# PREFIX
       		prefix="%03d_%s"%(f.getNewIdx3(),tcsstr)
	
              	counter_pin=Count(s,cnt_ch1,cnt_ch2)
               	cntstr=counter_pin.getPIN(3)

		logf.write("%5.3f %5.3f %s\n"%(tcsv,tcsh,cntstr))
		logf.flush()

	logf.close()
	shutter.close()
	exs1.closeV()

	break

s.close()
