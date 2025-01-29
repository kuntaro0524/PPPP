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
    en_list=[8.5,12.398,20.0]
    z2_list=[1800,2000,2200]
    tcs_list=[0.10]

# Dtheta scan range
    dtstart=-88000
    dtend=-83000
    dtstep=20
    dtch=3

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
		# slit1 full open
		exs.fullOpen()

		# Setting Z2
		mono.moveZ2(z2)
		z2str="%dpls"%z2

		for tcs_apert in tcs_list:
			tcsstr="tcs%fmm"%tcs_apert

			tcs.setApert(tcs_apert,tcs_apert)

			## Dtheta1
			prefix="%02d_%s_%s_%s"%(f.getNewIdx3("scn"),enstr,z2str,tcsstr)
			dt1_center=mono.scanDt1(prefix,dtstart,dtend,dtstep,dtch,0,0.2)

			# Slit1 vertical & horizontal scan
			prefix="%02d_%s_%s_%s"%(f.getNewIdx3("scn"),enstr,z2str,tcsstr)
			exs.fullOpen()
			slit1_vcenter=exs.scanV(prefix,18010,10,-100,dtch,0,0.2)
			slit1_hcenter=exs.scanH(prefix,-18010,-10,100,dtch,0,0.2)

			# log file
			logf.write("%8.2f keV Z2=%8d TCS apert %5.2fmm Dtheta1=%8.2f Exslit1(V,H)=(%8.2f,%8.2f)\n"%(en,z2,tcs_apert,dt1_center,slit1_vcenter,slit1_hcenter))
			logf.flush()

			# Axes information 
			prefix="%02d_%s_%s_%s"%(f.getNewIdx3("scn"),enstr,z2str,tcsstr)
			ofile=prefix+"_axes.dat"
			axes.all(ofile)

    logf.close()
    s.close()

    break
