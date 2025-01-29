#!/bin/env python 
import sys
import socket
import datetime
import time

# My library
from Received import *
from Organizer import *

from Dtheta import *
from FES import *
from ID import *
from TCS import *
from AxesInfo import *
from ExSlit1 import *


# Waiting the previous run
#time.sleep(2400)

host = '172.24.242.41'
port = 10101
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))

while True:
    print "start index:"
    data_index=int(raw_input())
# List
    #jenergy_list=[12.398, 8.5, 9.0, 10.0, 11.0, 14.0, 15.0, 16.0, 17.0, 18.0, 20.0]
    energy_list=[12.398]

# Observation time for each energy
    obstime=7200
# Interval time (sec)
    interval=10

# Counter
    ch_pin=2
    ch_ic=1

# Constructor
    stmono=Organizer(s,"bl_32in","tc1_stmono_1","")
    tcs=TCS(s)
    id=ID(s)
    dtune=DthetaTune(s)
    exslit1=ExSlit1(s,ch_pin)
    axes=AxesInfo(s)

# Initialization
    tcs.setApert(1.0,1.0)
    exslit1.fullOpen()

# Setting
    #data_index=0

    for e in energy_list:
	for i in range(0,50):
	# energy string
		en_str="%-8.3f"%float(e)
	# Prefix setting
		prefix="%02d_mono_%skeV_before" % (data_index,en_str.strip())
	# Output file open
		ofile=prefix+"_fixed.scn"
    		of=open(ofile,"w")
	# Moving monochro 
		stmono.move(e,"kev")
	# Moving ID
		id.moveE(e)
	# Dtheta1 tune
		dtune.do(prefix,ch_pin,ch_ic)
	# Slit1 scan
		exslit1.scanBoth(prefix)
	# Storing axes information
		tmp=prefix+"_axes.dat"
		axes.all(tmp)
	# Counter
		ntime=int(obstime/interval)
		starttime=datetime.datetime.now()
		of.write("%s"%starttime)

		for sec in range(0,ntime):
			tmpcnt=stmono.getCount(ch_pin,1.0)
			obstime=datetime.datetime.now()
			timestr="%8.3f"%(obstime-starttime).seconds

			of.write("%s %s %12d\n"%(obstime,timestr,tmpcnt))
			of.flush()
			time.sleep(interval)

		prefix="%02d_mono_%skeV_after" % (data_index,en_str.strip())
	# Slit1 scan
		exslit1.scanBoth(prefix)
	# Dtheta1 tune
		dtune.do(prefix,ch_pin,ch_ic)
	# Slit1 scan
		prefix="%02d_mono_%skeV_final" % (data_index,en_str.strip())
		exslit1.scanBoth(prefix)
	# Storing axes information
		tmp=prefix+"_axes.dat"
		axes.all(tmp)

		of.close()
		data_index+=1
    break
