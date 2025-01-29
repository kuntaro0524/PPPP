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
        sx=3.960
        sy=-13.1562
        sz=-0.6130

## 	Gonio rough position (FWHM center) [um]
	default_y=-13017
	default_z=-451

## 	Energy list
	enlist=[8.5,12.3984,18.0]

## 	TCS aperture list
	tcs_list=[(0.245,0.040,0.2,0.2)] # square 1x10um

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
		# Energy change
		mono.changeE(en)
		id.moveE(en)
		# Prefix of prefix
		prepre="e%05.2f"%en

		if en==8.5:
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
	
			ssec=float(tcs_param[3])
       			zwidth,zcenter=gonio.scanZenc(prefix,zstart,zend,gstep,cnt_ch1,cnt_ch2,ssec)

			# Flux measurements
                	# PIN counter
			gonio.moveXYZmm(sx,sy,sz)
                	counter_pin=Count(s,cnt_ch1,cnt_ch2)
                	cntstr=counter_pin.getPIN(3)

			logf.write("%8.2f,%5.3f,%5.3f,%8.3f,%8.3f,%8.3f,%8.3f,%s\n"%(en,tcsv,tcsh,zwidth,zcenter,ywidth,ycenter,cntstr))
			logf.flush()
			tcs_index+=1
			#if tcs_index==2:
				#print "Please set PICOAN to 1E3 gain and [Enter]"
				#ttt=raw_input()
	logf.close()
	exs1.closeV()

	break

s.close()
