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
	#host = '192.168.163.1'
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
        sx=3.5700
        sy=-13.1043
        sz=-0.4372

## 	Gonio rough position (FWHM center) [um]
	default_y=-12930
	default_z=-281

## 	Energy list
	enlist=[12.3984]

## 	TCS aperture list
	#tcs_list=[(0.026,0.04,0.1,1.0),(0.122,0.216,0.1,1.0),(0.245,0.5,0.5,0.2),(0.5,0.5,1.0,0.2),(1.0,1.0,1.0,0.2) ] # square 1um x 1.5um, 5um x 5um, 10um x 10um # 1st
	# For plotting Horizontal at fixed V (0.1)
	tcs_list=[(0.1,0.04,0.1,1.0),(0.1,0.08,0.1,1.0),(0.1,0.16,0.5,1.0),(0.1,0.32,1,0.5),(0.1,0.5,1,0.2),(0.1,1.0,1,0.2)]

## 	Log file
	logf=open("wire.log","w")

##	Counter channel
	cnt_ch1=3
	cnt_ch2=0

## 	Preparing gonio information (reset encoder)
	exs1.openV()
	gonio.prepScan()

## 	Wire scan
	step_num=50 # 

	for en in enlist:
		# Energy change
		mono.changeE(en)
		id.moveE(en)
		# Prefix of prefix
		prepre="e%05.2f"%en

		if en < 11.0:
			##	dtheta
        		prefix="%03d_%s"%(f.getNewIdx3(),prepre)
        		mono.scanDt1PeakConfig(prefix,"DTSCAN_LOWENERGY",tcs)

		else:
			##	dtheta
        		prefix="%03d_%s"%(f.getNewIdx3(),prepre)
        		mono.scanDt1PeakConfig(prefix,"DTSCAN_NORMAL",tcs)

		tcs_index=0
		for tcs_param in tcs_list:
			#if tcs_index==0:
				#print "Please set PICOAN to 1E4 gain and [Enter]"
				#raw_input()
			# TCS aparture
			tcsv=float(tcs_param[0])
			tcsh=float(tcs_param[1])
			gstep=float(tcs_param[2])
	
			# TCS set aperture
			tcs.setApert(tcsv,tcsh)
	
			# TCS str
			tcsstr="%4.3fx%4.3f"%(tcsv,tcsh)
	
			# PREFIX
       			prefix="%03d_%s_%s"%(f.getNewIdx3(),prepre,tcsstr)
	
			# range
			ystart=default_y-float(step_num)*gstep
			yend=default_y+float(step_num)*gstep
			zstart=default_z-float(step_num)*gstep
			zend=default_z+float(step_num)*gstep
	
			# set position
			gonio.moveXYZmm(sx,sy,sz)
			ssec=float(tcs_param[3])
       			ywidth,ycenter=gonio.scanYenc(prefix,ystart,yend,gstep,cnt_ch1,cnt_ch2,ssec)
			gonio.moveXYZmm(sx,sy,sz)
	
			# Flux measurements
                	# PIN counter
			gonio.moveXYZmm(sx,sy,sz)
                	counter_pin=Count(s,cnt_ch1,cnt_ch2)
                	cntstr=counter_pin.getPIN(3)

			logf.write("%8.2f,%5.3f,%5.3f,%8.3f,%8.3f,%s\n"%(en,tcsv,tcsh,ywidth,ycenter,cntstr))
			logf.flush()
			tcs_index+=1
			#if tcs_index==2:
				#print "Please set PICOAN to 1E3 gain and [Enter]"
				#ttt=raw_input()
	logf.close()
	exs1.closeV()

	break

s.close()
