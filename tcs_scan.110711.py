#!/bin/env python 
import sys
import socket
import time
import datetime

# My library
from Mono import *
from FES import *
from ID import *
from TCS import *
from ExSlit1 import *
from AxesInfo import *
from File import *

host = '172.24.242.41'
port = 10101
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))

while True:

# Conditions
    en_list=[12.3984]
    ty1_list=[3340,3140,3540]

# TCS scan range 110406
    scan_apert=0.05
    scan_another_apert=0.5
    scan_start=-2.0
    scan_end=2.0
    scan_step=0.05
    scan_time=0.2

# Detector number
    cnt_ch1=3
    cnt_ch2=0

# Devices
    id=ID(s)
    mono=Mono(s)
    tcs=TCS(s)
    exs=ExSlit1(s)
    axes=AxesInfo(s)
    f=File("./")

    index=0
    sizei=0

    # Log file
    logf=open("tcs_scan.log","w")
    logf.write("Gap[mm],Energy[kev],Dtheta1[pulse],Ty1[pulse],TCS_v,TCS_h,ESlit1_v,Eslit1_h\n")

    for en in en_list :
	# Axes information 
	prefix="%03d"%f.getNewIdx3()
	enstr="%fkev"%en
	ofile=prefix+"_"+enstr+"_axes.dat"
	axes.all(ofile)

	# Changing Energy
    	id.moveE(en)
    	mono.changeE(en)

	# Waiting for a thermal equilibrium
	#if en<12.398:
		#time.sleep(1800)

	for ty1 in ty1_list:
		# slit1 full open
		exs.fullOpen()

		# Setting Ty1
		mono.moveTy1(ty1)

		##  dtheta1 tune @ TCS 3.0mm x 3.0mm
		tcs.setApert(3.0,3.0)

		## Dtheta1
		prefix="%03d_tcs_fo"%f.getNewIdx3()
		dt1_fwhm,dt1_center=mono.scanDt1PeakConfig(prefix,"DTSCAN_NORMAL",tcs)

		# TCS vertical & horizontal scan x 1times
    		prefix="%03d_tcs"%f.getNewIdx3()
    		vcenter1,tmp=tcs.scanVrel(prefix,0.05,0.5,1.4,scan_step,cnt_ch2,cnt_ch1,scan_time)
    		hcenter1,tmp=tcs.scanHrel(prefix,0.50,0.05,1.4,scan_step,cnt_ch2,cnt_ch1,scan_time)

		# TCS aperture 0.1x0.1mm
		tcs.setApert(0.1,0.1)

		# Slit1 vertical & horizontal scan
    		prefix="%03d"%f.getNewIdx3()
		exs.fullOpen()

		slit1_hfwhm,slit1_hcenter=exs.scanH(prefix,-slit1_start,-slit1_end,-slit1_step,slit1_ch0,slit1_ch1,0.5)

		# Log string
		#("Gap[mm],Energy[kev],Dtheta1[pulse],Ty1[pulse],TCS_v,TCS_h,Eslit1_h")
		logstr="%8.3f,%8.3f,%8d,%8d,%7.4f,%7.4f,%8.1f"%(id.getE(en),en,dt1_center,ty1,vcenter1,hcenter1,slit1_hcenter)
		logf.write("%s\n"%logstr)
		logf.flush()

		# Axes information 
		prefix="%03d_final"%f.getNewIdx3()
		ofile=prefix+"_axes.dat"
		axes.all(ofile)

    logf.close()
    s.close()

    break
