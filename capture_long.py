#!/bin/env python 
import sys
import socket
import time
import datetime
import os

# My library
from BeamCenter import *
from Capture import *
from Mono import *
from ExSlit1 import *
from  File import *
from TCS import *

if __name__=="__main__":

	host = '172.24.242.41'
	port = 10101
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host,port))

	tcs=TCS(s)
	cap=Capture()
	mono=Mono(s)
	slit1=ExSlit1(s)
	f=File("./")

	dire=os.getcwd()

        # pixel to micron [um/pixel] in high zoom
        p2u_z=7.1385E-2
        p2u_y=9.770E-2

	idx=0

	starttime=time.time()

	of=open("Captured.dat","w")

	interval_time=3600 #[sec]

	for i in range(0,48):
		# Dtheta tune 
		prefix="%03d"%f.getNewIdx3()
		mono.scanDt1PeakConfig(prefix,"DTSCAN_NORMAL",tcs)
		dtheta1=int(mono.getDt1())

		# Slit open
		slit1.openV()

		filename="%s/%03d_cap.ppm"%(dire,i)
		x,y=cap.captureBM(filename)
		h_um=x*p2u_y
		v_um=y*p2u_z

		tmptime=time.time()
		dtime=tmptime-starttime

		jikan=datetime.datetime.now()
		print jikan
		of.write("%10s %12.2f %10s %5d %5.2f %5.2f %5.3f %5.3f\n"%(jikan,dtime,filename,dtheta1,x,y,h_um,v_um))
		of.flush()
		
		# Slit close
		slit1.closeV()

		# interval
		time.sleep(interval_time)

	slit1.closeV()
	of.close()
