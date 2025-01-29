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
from FES import *
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
	fes=FES(s)
	tcs=TCS(s)
	conf=ConfigFile()
	colli=Colli(s)
	f=File("./")
	exs1=ExSlit1(s)
	shutter=Shutter(s)

## 	Gonio set position [mm]
        sx=-0.3908
        sy=-12.2531
        sz=0.5310

## 	Energy list
	#enlist=[18.5,17.5,16.5,15.5,14.5,13.5,12.3984,11.5,10.5,9.5,8.5]
	#enlist=[12.3984,18.0,8.5]
	enlist=[12.3984, 18.0, 8.5]

## 	FES aperture list
	# 1x10um beam
	fes_list=[(0.3,0.3),(0.2,0.2),(0.15,0.15),(0.12,0.12),(0.1,0.1),(0.08,0.08),(0.07,0.07),(0.06,0.06)]

## 	Log file
        logname="%03d_wire.log"%(f.getNewIdx3())
	logf=open(logname,"w")

##	Counter channel
	cnt_ch1=3
	cnt_ch2=0

## 	Preparing gonio information (reset encoder)
	gonio.prepScan()

## 	Counter
        counter_pin=Count(s,cnt_ch1,cnt_ch2)

	fesv=float(0.3)
	fesh=float(0.3)
	fes.setApert(fesv,fesh)

#	Dtheta tune
	dthetaTuneFlag=True

## 	Wire scan
	for en in enlist:
		# Energy change
		mono.changeE(en)
		id.moveE(en)
		# Prefix of prefix
		prepre="e%07.3f"%en

		fesv=float(0.3)
		fesh=float(0.3)
		fes.setApert(fesv,fesh)
		
		if dthetaTuneFlag:
			# 8.5keV 15min for thermal equilibrium
			if en<=10.0:
				time.sleep(900)
			if en > 10.0:
        			prefix="%03d_%s"%(f.getNewIdx3(),prepre)
        			mono.scanDt1PeakConfig(prefix,"DTSCAN_FULLOPEN",tcs)
        			#mono.scanDt1PeakConfig(prefix,"DTSCAN_NORMAL",tcs)
			elif en <= 10.0:
        			prefix="%03d_%s"%(f.getNewIdx3(),prepre)
        			mono.scanDt1PeakConfig(prefix,"DTSCAN_FULLOPEN",tcs)
        			#mono.scanDt1PeakConfig(prefix,"DTSCAN_LOWENERGY",tcs)
		## Collimator scan
		## evacuation of a wire
		gonio.moveXYZmm(sx,sy,sz)
        	prefix="%03d_colli"%(f.getNewIdx3())
		colli_y,colli_z=colli.scan(prefix,3) #PIN after sample position
                cntstr_colli=counter_pin.getPIN(3)

		## Wire rough scan
		xp,zp=gonio.wireRoughZ(3)
		yp=gonio.wireRoughY(3)

		# mm -> um
		xp=xp*1000.0
		yp=yp*1000.0
		zp=zp*1000.0

		print "##### Wire Rough %8.5f %8.5f %8.5f\n"%(xp,yp,zp)

		for fes_param in fes_list:
			# FES aparture
			fesv=float(fes_param[0])
			fesh=float(fes_param[1])
	
			# FES set aperture
			fes.setApert(fesv,fesh)
	
			# FES str
			fesstr="%4.3fx%4.3f"%(fesv,fesh)
	
			# PREFIX
       			prefix="%03d_%s_%s"%(f.getNewIdx3(),prepre,fesstr)

			# Check FES aperture Horizontal
			if fesh < 0.1:
				gstep_y=0.1
				ssec_y=1.0
				nstep_y=100 # 
			elif fesh < 0.7:
				gstep_y=0.5
				ssec_y=1.0
				nstep_y=25 # 

			# Check FES aperture Vertical
			if fesv < 0.10:
				gstep_z=0.2
				ssec_z=1.0
				nstep_z=100 # 
			elif fesv < 0.70:
				gstep_z=0.5
				ssec_z=1.0
				nstep_z=50 # 
	
			# range
			ystart=yp-float(nstep_y)*gstep_y
			yend=yp+float(nstep_y)*gstep_y
			zstart=zp-float(nstep_z)*gstep_z
			zend=zp+float(nstep_z)*gstep_z
	
			# set position
			gonio.moveXYZmm(sx,sy,sz)
       			ywidth,ycenter=gonio.scanYenc(prefix,ystart,yend,gstep_y,cnt_ch1,cnt_ch2,ssec_y)

			gonio.moveXYZmm(sx,sy,sz)
       			zwidth,zcenter=gonio.scanZenc(prefix,zstart,zend,gstep_z,cnt_ch1,cnt_ch2,ssec_z)

			# Flux measurements
                	# PIN counter
			gonio.moveXYZmm(sx,sy,sz)
                	cntstr=counter_pin.getPIN(3)

			logf.write("%8.4f %5.1f %5.1f %5.3f %5.3f %8.3f %8.3f %8.3f %8.3f %s (colli: %s)\n"%(en,colli_y,colli_z,fesv,fesh,zwidth,zcenter,ywidth,ycenter,cntstr,cntstr_colli))
			logf.flush()
	logf.close()#
	exs1.closeV()

	break

s.close()
