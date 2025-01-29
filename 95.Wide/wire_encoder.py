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
	prefix="%03d"%f.getNewIdx3()

## 	Preparing gonio information
	gonio.prepScan()

##	Wire scan range
####	Rough scan
	
	#center=gonio.scanZ(prefix,-10550,-10350,5,cnt_ch1,cnt_ch2,0.2)

	break

	#logf.close()

s.close()
