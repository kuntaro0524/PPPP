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
    en_list=[12.398,8.5,20.0]
    z2_list=[2000,1500,1000]

# Dtheta scan range
    scan_dt1_start=-88000
    scan_dt1_end=-83000
    scan_dt1_step=20
    scan_dt1_ch=0

# TCS scan parameters
    scan_apert=0.05
    scan_another_apert=0.5
    scan_start=-1.0
    scan_end=1.0
    scan_step=0.05
    scan_time=0.2
    tcs_scanch1=3 # PIN before mirror
    tcs_scanch2=0 # IC before mirror

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
    logf=open("fix.log","w")

    for en in en_list :
	# Axes information 
	prefix="%03d"%f.getNewIdx3()
	enstr="%fkev"%en
	ofile=prefix+"_"+enstr+"_axes.dat"
	axes.all(ofile)

	# Changing Energy
	if en==8.5:
		id.move(7.62)
	else:
    		id.moveE(en)

    	mono.changeE(en)

	for z2 in z2_list:

		# Setting Z2
		mono.moveZ2(z2)
		z2str="%-dpulse"%z2
	
		# TCS FO
		tcs.setApert(3.0,3.0)

		## Dtheta1
		idx=f.getNewIdx3()
		prefix="%03d_%s_%s"%(idx,enstr,z2str)
		junk,dt1_center=mono.scanDt1PeakBackLash(prefix,scan_dt1_start,scan_dt1_end,scan_dt1_step,scan_dt1_ch,0,0.2)

		## TCS scan
		## 1st
		idx=f.getNewIdx3()
		prefix="%03d_%s_%s_1st"%(idx,enstr,z2str)
		tcs.scanBoth(prefix,scan_apert,scan_another_apert,scan_start,scan_end,scan_step,tcs_scanch1,tcs_scanch2,scan_time)

		## 2nd
		idx=f.getNewIdx3()
		prefix="%03d_%s_%s_2nd"%(idx,enstr,z2str)
		vcen,hcen=tcs.scanBoth(prefix,scan_apert,scan_another_apert,scan_start,scan_end,scan_step,tcs_scanch1,tcs_scanch2,scan_time)

		## St1Slit1 vertical and horizontal scan
                # Slit1 vertical & horizontal scan
                prefix="%02d_%s_%s"%(f.getNewIdx3(),enstr,z2str)

                exs.fullOpen()
                slit1_vcenter=exs.scanV(prefix,18010,10,-100,3,0,0.2)[1]
                slit1_hcenter=exs.scanH(prefix,-18010,-10,100,3,0,0.2)[1]

		# log file
		logf.write("%8.2f,%8d,%8d,%8.3f,%8.3f\n"%(en,z2,dt1_center,vcen,hcen,slit1_vcenter,slit1_hcenter))
		logf.flush()

		# Axes information 
		idx=f.getNewIdx3()
		prefix="%03d_%s_%s_final"%(idx,enstr,z2str)
		ofile=prefix+"_axes.dat"
		axes.all(ofile)

    logf.close()
    s.close()

    break
