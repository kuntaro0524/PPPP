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
	f=File("./")
	exs1=ExSlit1(s)

## 	Gonio set position [mm]
        sx=3.80
        sy=-13.1481
        sz=-0.4989

## 	Gonio rough position (FWHM center) [um]
	default_y=-13018
	default_z=-342

## 	Energy list
	#enlist=[12.3984,18.0,8.5]
	enlist=[8.5,12.3984,18.0]

## 	TCS aperture list
	tcs_list=[(0.245,0.040,1.0,1.0)] # square 1um x 1.5um, 5um x 5um, 10um x 10um # 1st
## 	Log file
	logf=open("wire.log","w")

##	Counter channel
	cnt_ch1=3
	cnt_ch2=0

## 	Preparing gonio information (reset encoder)
	exs1.openV()
	gonio.prepScan()

## 	Wire scan
	step_num=100 # 

	for en in enlist:
		mono.changeE(en)
		id.moveE(en)
		prepre="e%05.2f"%en
        	prefix="%03d_%s"%(f.getNewIdx3(),prepre)
        	mono.scanDt1PeakConfig(prefix,"DTSCAN_NORMAL",tcs)

		for tcs_param in tcs_list:
                        # TCS aparture
                        tcsv=float(tcs_param[0])
                        tcsh=float(tcs_param[1])
                        gstep=float(tcs_param[2])

			# TCS set aperture
			tcs.setApert(tcsv,tcsh)
	
                	# PIN counter
			gonio.moveXYZmm(sx,sy,sz)
                	counter_pin=Count(s,cnt_ch1,cnt_ch2)
                	cntstr=counter_pin.getPIN(3)

			logf.write("%8.2f,%5.3f,%5.3f,%s\n"%(en,tcsv,tcsh,cntstr))
			logf.flush()
	logf.close()
	exs1.closeV()

	break

s.close()
