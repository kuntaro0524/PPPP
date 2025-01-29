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
	sx=3.6349
	sy=-13.1045
	sz=-0.8742

## 	Gonio rough position (FWHM center) [um]
	## EX) default_y=-12955
	## EX) default_z=-953
	default_y=-12965
	default_z=-705

## 	Energy list
	enlist=[12.3984,18.0]

## 	TCS aperture list
	# Itsumono
	tcs_list=[(0.026,0.043,0.1),(0.1220,0.216,0.5),(0.2450,0.50,1.0)]

## 	Log file
	logf=open("wire.log","w")

##	Counter channel
	cnt_ch1=3
	cnt_ch2=0

## 	Preparing gonio information (reset encoder)
	gonio.prepScan()

## 	Wire scan
	step_num=50 # 

	for en in enlist:
		# Energy change
		mono.changeE(en)
		id.moveE(en)
		# Prefix of prefix
		prepre="e%05.2f"%en
		
		# 8.5keV 15min for thermal equilibrium
		if en<10.0:
			time.sleep(900)

		##	dtheta
        	prefix="%03d_%s"%(f.getNewIdx3(),prepre)
        	mono.scanDt1PeakConfig(prefix,"DTSCAN_NORMAL",tcs)

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
       			prefix="%03d_%s_%s"%(f.getNewIdx3(),prepre,tcsstr)
	
			# range
			ystart=default_y-float(step_num)*gstep
			yend=default_y+float(step_num)*gstep
			zstart=default_z-float(step_num)*gstep
			zend=default_z+float(step_num)*gstep
	
			# set position
			gonio.moveXYZmm(sx,sy,sz)
       			ywidth,ycenter=gonio.scanYenc(prefix,ystart,yend,gstep,cnt_ch1,cnt_ch2,1.0)
			gonio.moveXYZmm(sx,sy,sz)
	
       			zwidth,zcenter=gonio.scanZenc(prefix,zstart,zend,gstep,cnt_ch1,cnt_ch2,1.0)

			# Flux measurements
                	# PIN counter
			gonio.moveXYZmm(sx,sy,sz)
                	counter_pin=Count(s,cnt_ch1,cnt_ch2)
                	cntstr=counter_pin.getPIN(4)

			logf.write("%8.2f,%5.3f,%5.3f,%8.3f,%8.3f,%8.3f,%8.3f,%s\n"%(en,tcsv,tcsh,zwidth,zcenter,ywidth,ycenter,cntstr))
			logf.flush()
	logf.close()
	exs1.closeV()

	break

s.close()
