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
from TCS import *
from ConfigFile import *
from Count import *
from ExSlit1 import *
from Colli import *
from Shutter import *

while True:
	host = '172.24.242.41'
	port = 10101
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host,port))

##	Device definition
	id=ID(s)
	mono=Mono(s)
	gonio=Gonio(s)
	tcs=TCS(s)
	conf=ConfigFile()
	colli=Colli(s)
	f=File("./")
	exs1=ExSlit1(s)
	shutter=Shutter(s)

## 	Energy list
	#enlist=[18.0,15.0,12.3984,10.5,8.5]
	enlist=[8.5,10.0,12.3984,15.0,18.0]

	# 5x10um
	tcs_list=[(0.1,0.1)]

## 	Log file
	logf=open("flux.log","w")

##	Counter channel
	cnt_ch1=3
	cnt_ch2=0

## 	Counter
        counter_pin=Count(s,cnt_ch1,cnt_ch2)

## 	Wire scan
	for en in enlist:
		# Energy change
		mono.changeE(en)
		id.moveE(en)

		# Prefix of prefix
		prepre="e%07.3f"%en
		
		# 8.5keV 15min for thermal equilibrium
		if en<10.0:
			time.sleep(10)

		##	dtheta
		## Energy > 10.0
		if en > 10.0:
        		prefix="%03d_%s"%(f.getNewIdx3(),prepre)
        		mono.scanDt1PeakConfig(prefix,"DTSCAN_NORMAL",tcs)
		elif en <= 10.0:
        		prefix="%03d_%s"%(f.getNewIdx3(),prepre)
        		mono.scanDt1PeakConfig(prefix,"DTSCAN_LOWENERGY",tcs)

		for tcs_param in tcs_list:
			# TCS aparture
			tcsv=float(tcs_param[0])
			tcsh=float(tcs_param[1])
	
			# TCS set aperture
			tcs.setApert(tcsv,tcsh)
	
			# PREFIX
       			prefix="%03d_%s"%(f.getNewIdx3(),prepre)

			# Flux measurements
                	# PIN counter
                	cntstr=counter_pin.getPIN(3)

			logf.write("%8.4f %5.3f %5.3f  %s\n"%(en,tcsv,tcsh,cntstr))
			logf.flush()
	logf.close()
	#exs1.closeV()

	break

s.close()
