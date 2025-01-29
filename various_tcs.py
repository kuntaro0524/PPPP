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
    en_list=[8.5,10,11,12.398,14,16,18,20]
    tcs_apert_list=[0.05,0.10,0.20,0.30,0.40,0.50]

# Dtheta scan range
    dtstart=-92000
    dtend=-88000
    dtstep=20

# Detector number
    cnt_ch1=3
    cnt_ch2=1

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
    logf=open("various_tcs.log","w")

    for en in en_list :
	# Axes information 
	prefix="%02d_before.dat"%f.getNewIdx("scn")
	enstr="%fkev"%en
	ofile=prefix+"_"+enstr+"_axes.dat"
	axes.all(ofile)

	# Changing Energy
	if en==8.5:
		id.move(7.62)
	else:
    		id.moveE(en)

    	mono.changeE(en)

	for apert in tcs_apert_list:

		# slit1 full open
		exs.fullOpen()

		# TCS aperture
		tcs.setApert(apert,apert)
	
		## Dtheta1
		prefix="%02d_tcs%-5.2fmm"%(f.getNewIdx("scn"),apert)
		dt1_center=mono.scanDt1(prefix,dtstart,dtend,dtstep,cnt_ch1,cnt_ch2,0.2)
	
		# Slit1 vertical & horizontal scan
		prefix="%02d_tcs%-5.2fmm"%(f.getNewIdx("scn"),apert)
		exs.fullOpen()
		slit1_vcenter=exs.scanV(prefix,18010,10,-100,cnt_ch1,1,0.2)
		slit1_hcenter=exs.scanH(prefix,-18010,-10,100,cnt_ch1,1,0.2)
	
		# log file
		logf.write("%8.2f keV aperture %5.2fmm Dtheta1=%8d Exslit1(V,H)=(%8d,%8d)\n"%(en,apert,int(dt1_center),int(slit1_vcenter),int(slit1_hcenter)))
		logf.flush()

	# Axes information 
	prefix="%02d_final"%f.getNewIdx("scn")
	ofile=prefix+"_axes.dat"
	axes.all(ofile)

    logf.close()
    s.close()

    break
