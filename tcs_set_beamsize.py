#!/bin/env python 
import sys
import socket
import time
import datetime

# My library
from TCS import *
from Mono import *
from AxesInfo import *

if __name__=="__main__":
        host = '172.24.242.41'
        port = 10101
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host,port))

        tcs=TCS(s)
	mono=Mono(s)

	print "Choose \n Large/Medium/Small\n"
	print "(### Large  (HxV)=(12x6) ### (Medium (HxV)=(3x2)) ### (Small  (HxV)=(2x1))"

	com=raw_input()	

	if com=="Large" or com=="L":
		height=0.5
		width=0.5

	elif com=="Medium" or com=="M":
		height=0.1
		width=0.1

	elif com=="Small" or com=="S":
		height=0.026
		width=0.040
	else:
		print "Unknown"
		System.exit(1)
		
	#####
	print height , width
	tcs.setApert(height,width)

	#####
	f=File("./")
	new=f.getNewIdx(".scn")
	prefix="%5d"%new
	step=50
        mono.scanDt1(prefix,-92000,-86000,step,2,0,0.2)

	##### 
	new=f.getNewIdx(".dat")

	ofile="%5d_axes.dat"%new

	ax=AxesInfo("")	
	ax.all(ofile)

        s.close()
