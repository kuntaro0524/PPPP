#!/bin/env python import sys
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
from Cover import *

##	Usefull function
def wire_rough_scan(sx,sy,sz): #sx,sy,sz = wire default
	## Wire rough scan
	ssz = sz + 0.1
	gonio.moveXYZmm(sx,sy,ssz)
	xp,zp=gonio.wireRoughZ(3)
	ssy = sy + 0.1
	gonio.moveXYZmm(sx,ssy,sz)
	yp=gonio.wireRoughY(3)

	# mm -> um
	xp=xp*1000.0
	yp=yp*1000.0
	zp=zp*1000.0
	print "##### Wire Rough %8.5f %8.5f %8.5f\n"%(xp,yp,zp)

	return xp,yp,zp

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
	colli=Colli(s)
	f=File("./")
	exs1=ExSlit1(s)
	shutter=Shutter(s)

	covz=Cover(s)

## 	Gonio set position [mm]
	sx=0.6288
	sy=-10.6894
	sz=-0.4716

## 	Prep scan
	print "CCD cover moves to close position"
	covz.on()
	print "Ex1 slit moves to close position"
	exs1.closeV()
	print "Shutter close"
	shutter.close()

## 	Energy list
#	enlist=[8.5,10.5,12.3984,15.5,18.5]
#	enlist=[10.5,15.5,18.5]
	enlist=[8.7,10.5,12.3984,15.5,18.0]

## 	TCS aperture list
	# Itsumono
	# Normally used
	tcs_list=[(0.026,0.040),(0.05,0.05),(0.1,0.1),(0.15,0.15),(0.2,0.2),(0.3,0.3),(0.5,0.5),(1.0,1.0),(0.5,0.04),(1.0,0.04)]

## 	Log file
        logname="%03d_wire.log"%(f.getNewIdx3())
	logf=open(logname,"w")

##	Counter channel
	cnt_ch1=3
	cnt_ch2=0

## 	Preparing gonio information (reset encoder)
	#gonio.prepScan() # deleted by K.Hirata 140624

## 	Counter
        counter_pin=Count(s,cnt_ch1,cnt_ch2)

#	Dtheta tune
	dthetaTuneFlag=True
	#dthetaTuneFlag=False

## 	Wire scan
	for en in enlist:
		# Energy change
		mono.changeE(en)
		id.moveE(en)
#		time.sleep(900)
		# Prefix of prefix
		prepre="e%07.3f"%en
		
		if dthetaTuneFlag:
			# 8.5keV 15min for thermal equilibrium
			if en == 8.5:
				print "E=8.5keV"
			elif en<=10.0:
				print "Please remove # for the true one"
				time.sleep(3)
				#time.sleep(900)
	
			# Delta theta1 tune
			# Lower/Higher energy No dtheta1 offset.
       			prefix="%03d_%s"%(f.getNewIdx3(),prepre)
       			mono.scanDt1PeakConfig(prefix,"DTSCAN_NORMAL",tcs)

		# Prep scan
		print "Ex1 slit moves to open position"
		exs1.openV()
		print "Shutter open"
		shutter.open()
		
		## Collimator scan
		## evacuation of a wire
		gonio.moveXYZmm(sx,sy,sz)
        	prefix="%03d_colli"%(f.getNewIdx3())
		colli_y,colli_z=colli.scan(prefix,3) #PIN after sample position
                cntstr_colli=counter_pin.getPIN(3)
		trans,pin=colli.compareOnOff(3)

		for tcs_param in tcs_list:
			# Prep scan (All shutter is closed when the wire scan finished)
			# They should be opened here for loop experiments
			print "Ex1 slit moves to open position"
			exs1.openV()
			print "Shutter open"
			shutter.open()

			# TCS aparture
			tcsv=float(tcs_param[0])
			tcsh=float(tcs_param[1])
	
			# TCS set aperture
			tcs.setApert(tcsv,tcsh)
	
			# TCS str
			tcsstr="%4.3fx%4.3f"%(tcsv,tcsh)
	
			# PREFIX
       			prefix="%03d_%s_%s"%(f.getNewIdx3(),prepre,tcsstr)

			# Check TCS aperture Horizontal
			if tcsh < 0.1:
				gstep_y=0.1
				ssec_y=2.0
				nstep_y=100 # 
			elif tcsh < 0.4:
				gstep_y=0.5
				ssec_y=2.0
				nstep_y=30 # 
			else :
				gstep_y=1.0
				ssec_y=2.0
				nstep_y=20 # 

			# Check TCS aperture Vertical
			if tcsv < 0.07:
				gstep_z=0.1
				ssec_z=2.0
				nstep_z=100 # 
			elif tcsv < 0.26:
				gstep_z=0.2
				ssec_z=2.0
				nstep_z=50 # 
			elif tcsv < 5.0:
				gstep_z=0.5
				ssec_z=2.0
				nstep_z=50 # 

			# Move wire to default position
			gonio.moveXYZmm(sx,sy,sz)
			# Wire rough scan
			xp,yp,zp=wire_rough_scan(sx,sy,sz) #sx,sy,sz = wire default
			print "Wire rough position: %10.2f %10.2f %10.2f [um]"%(xp,yp,zp)
	
			# range
			ystart=yp-float(nstep_y)*gstep_y
			yend=yp+float(nstep_y)*gstep_y
			zstart=zp-float(nstep_z)*gstep_z
			zend=zp+float(nstep_z)*gstep_z
			print "Scan Y range: %10.3f - %10.3f"%(ystart,yend)
			print "Scan Z range: %10.3f - %10.3f"%(zstart,zend)
	
			# set position
			print "Ytest"
       			ywidth,ycenter=gonio.scanYenc(prefix,ystart,yend,gstep_y,cnt_ch1,cnt_ch2,ssec_y)

			gonio.moveXYZmm(sx,sy,sz)
       			zwidth,zcenter=gonio.scanZenc(prefix,zstart,zend,gstep_z,cnt_ch1,cnt_ch2,ssec_z)

			# Flux measurements
                	# PIN counter
			gonio.moveXYZmm(sx,sy,sz)
                	cntstr=counter_pin.getPIN(3)
			logf.write("%8.4f %5.1f %5.1f %5.3f %5.3f %8.3f %8.3f %8.3f %8.3f %s ( colli: %s, Trans: %5.2f percent )\n"%(en,colli_y,colli_z,tcsv,tcsh,zwidth,zcenter,ywidth,ycenter,cntstr,cntstr_colli,trans))
			logf.flush()

			# Finishing scan before the next delta_theta1 tune
			print "Scan finished! Ex1 slit moves to close position"
			exs1.closeV()
			print "Scan finished! Shutter moves to close position"
			shutter.close()
	logf.close()
	exs1.closeV()
	id.moveE(12.3984)
	mono.changeE(12.3984)

	break
s.close()
