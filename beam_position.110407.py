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
    en_list=[12.398]

# St2Slit1 knife edge scan
    slit1_start=18010
    slit1_end=10
    slit1_step=-100
    slit1_ch0=3
    slit1_ch1=0

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
    logf=open("beamposition.log","w")
    logf.write("Gap[mm],Energy[kev],Dtheta1[pulse],ESlit1_v,Eslit1_h\n")

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

	# Waiting for a thermal equilibrium
	if en<12.398:
		time.sleep(600)
		print "12.398 ika"

	# slit1 full open
	exs.fullOpen()

	## Dtheta1
	#prefix="%03d_tcs_fo"%f.getNewIdx3()
	#dt1_fwhm,dt1_center=mono.scanDt1PeakConfig(prefix,"DTSCAN_NORMAL",tcs)

	# Slit1 vertical & horizontal scan
    	prefix="%03d"%f.getNewIdx3()
	exs.fullOpen()

	slit1_vfwhm,slit1_vcenter=exs.scanV(prefix,slit1_start,slit1_end,slit1_step,slit1_ch0,slit1_ch1,1.0)
	slit1_hfwhm,slit1_hcenter=exs.scanH(prefix,-slit1_start,-slit1_end,-slit1_step,slit1_ch0,slit1_ch1,0.5)

	# Log string
    	#"Gap[mm],Energy[kev],Dtheta1[pulse],ESlit1_v,Eslit1_h\n"
	logstr="%8.3f,%8.3f,%8d,%8.1f,%8.1f"%(id.getE(en),en,dt1_center,slit1_vcenter,slit1_hcenter)
	logf.write("%s\n"%logstr)
	logf.flush()

    logf.close()
    s.close()

    break
