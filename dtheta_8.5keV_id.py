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
    id_list=[7.50,7.55,7.60,7.61,7.62,7.63,7.64,7.65,7.66]

# Dtheta scan range
    dtstart=-92000
    dtend=-86000
    dtstep=100

# Detector number
    cnt_ch1=0
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
    logf=open("dtheta.log","w")

    for gap in id_list :
	# change ID
	id.move(gap)
	# Axes information 
	prefix="%02d"%f.getNewIdx("scn")
	idstr="%fmm"%gap
	ofile=prefix+"_"+idstr+"_axes.dat"
	axes.all(ofile)

	##  dtheta1 tune @ TCS 3.0mm x 3.0mm
	tcs.setApert(5.0,5.0)

	## Dtheta1
	prefix="%02d_%s"%(f.getNewIdx("scn"),idstr)
	dt1_center=mono.scanDt1(prefix,dtstart,dtend,dtstep,cnt_ch1,cnt_ch2,0.2)

	# log file
	logf.write("%8.2f mm Dtheta1=%8d \n"%(gap,int(dt1_center)))
	logf.flush()

	# Axes information 
	prefix="%02d_final"%f.getNewIdx("scn")
	ofile=prefix+"_axes.dat"
	axes.all(ofile)

    logf.close()
    s.close()

    break
