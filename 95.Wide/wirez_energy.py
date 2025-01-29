#!/bin/env python 
import sys
import socket
import time
import math
from pylab import *

# My library
from Gonio import *
from ID import *
from Mono import *

while True:
	host = '172.24.242.41'
	port = 10101
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host,port))

##	Device definition
	id=ID(s)
	mono=Mono(s)
	gonio=Gonio(s)
	f=File("./")

## 	Log file
	logf=open("wirez_en.log","w")

## 	dtheta1 tune range
    	dtstart=-92000
    	dtend=-88000
    	dtstep=50

##	Counter channel
	cnt_ch1=3
	cnt_ch2=2

##	Energy condition
	en_list=[10.5, 12.398, 16.0, 18.0]
		
	for en in en_list:
		# change energy
		id.moveE(en)
		mono.changeE(en)

		# tune dtheta1
		prefix="%02d"%f.getNewIdx("scn")
		dt1=mono.scanDt1(prefix,dtstart,dtend,dtstep,cnt_ch2,cnt_ch1,0.2)

		# gonio wire z scan
		prefix="%02d"%f.getNewIdx("scn")
		center=gonio.scanZ(prefix,-10550,-10350,5,cnt_ch1,cnt_ch2,0.2)

		# log file
		logf.write("%8.3f keV Dtheta1:%8.1f center: %8.3f [um]"%(float(en),dt1,center))
	break

	logf.close()

s.close()
