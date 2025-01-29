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

## 	Gonio set position [mm]
	sx=3.1765
	sy=-13.1151
	sz=-0.7048


## 	TCS aperture list
	tcs_list=[(0.026,0.04,0.1)]

## 	Log file
	logf=open("wire.log","w")

##	Counter channel
	cnt_ch1=3
	cnt_ch2=0

## 	Preparing gonio information (reset encoder)
	gonio.prepScan()

## 	Gonio rough position (FWHM center) [um]
	default_y=-12952
	default_z=-549

## 	scan range
	ystart=default_y-30
	yend=default_y+30
	zstart=default_z-30
	zend=default_z+30

##	dtheta
        try :
                ## Dtheta 1
                scan_dt1_ch1=int(conf.getCondition2("DTSCAN_NORMAL","ch1"))
                scan_dt1_ch2=int(conf.getCondition2("DTSCAN_NORMAL","ch2"))
                scan_dt1_start=int(conf.getCondition2("DTSCAN_NORMAL","start"))
                scan_dt1_end=int(conf.getCondition2("DTSCAN_NORMAL","end"))
                scan_dt1_step=int(conf.getCondition2("DTSCAN_NORMAL","step"))
                scan_dt1_time=conf.getCondition2("DTSCAN_NORMAL","time")
                tcsv=conf.getCondition2("DTSCAN_NORMAL","tcsv")
                tcsh=conf.getCondition2("DTSCAN_NORMAL","tcsh")

        except MyException,ttt:
                print ttt.args[0]
                print "Check your config file carefully.\n"
                sys.exit(1)

## 	Wire scan
	step_num=50 # 

	#dtheta1 tune
       	#prefix="%03d_dtheta1"%f.getNewIdx3()
       	#mono.scanDt1Peak(prefix,scan_dt1_start,scan_dt1_end,scan_dt1_step,scan_dt1_ch1,scan_dt1_ch2,scan_dt1_time)  #hashi 100628

	for tcs_param in tcs_list:
		# TCS aparture
		tcsv=float(tcs_param[0])
		tcsh=float(tcs_param[1])
		gstep=float(tcs_param[2])

		# TCS set aperture
		tcs.setApert(tcsv,tcsh)

		# TCS str
		tcsstr="%3.2fx%3.2f"%(tcsv,tcsh)

		# PREFIX
       		prefix="%03d_%s"%(f.getNewIdx3(),tcsstr)

		# range
		ystart=default_y-float(step_num)*gstep
		yend=default_y+float(step_num)*gstep
		zstart=default_z-float(step_num)*gstep
		zend=default_z+float(step_num)*gstep

		# set position
		gonio.moveXYZmm(sx,sy,sz)

       		ywidth,ycenter=gonio.scanYenc(prefix,ystart,yend,gstep,cnt_ch1,cnt_ch2,0.2)

		gonio.moveXYZmm(sx,sy,sz)

       		zwidth,zcenter=gonio.scanZenc(prefix,zstart,zend,gstep,cnt_ch1,cnt_ch2,0.2)

		# PIN counter
		counter_pin=Count(s,cnt_ch1,cnt_ch2)
		cntstr=counter_pin.getPIN(cnt_ch1,3)

		logf.write("%5.2f,%5.2f,%8.3f,%8.3f,%8.3f,%8.3f,%s\n"%(tcsv,tcsh,ywidth,ycenter,zwidth,zcenter,cntstr))
		logf.flush()

	logf.close()

	break

s.close()
