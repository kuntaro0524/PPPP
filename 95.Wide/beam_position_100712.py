#!/bin/env python 
import sys
import socket
import time

# My library
from ID import *
from TCS import *
from AxesInfo import *
from File import *
from Mono import *
from ExSlit1 import *


host = '172.24.242.41'
port = 10101
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))

while True:
	print "Input index [example. 00, 01,...]:"
 
	energy_list=[12.398] # 100708 kuntaro
	tcs_list=[(3.0,3.0)]

# Constructer
	stmono=Mono(s)
	tcs=TCS(s)
	id=ID(s)
	axes=AxesInfo(s)
	f=File("./")
	exs1=ExSlit1(s)

# Counter <-> channel
	ic=0	# I0
	pin2=2	# Pin photodiode in chamber
	pin3=3	# pin photodiode after sample

# Dtheta1 tune parameters
	dt_start=-95000
	dt_end=-90000
	dt_step=50
	dt_cnt=0.2
	dt_main=3
	dt_sub=0

# St2Slit1 knife edge scan
	slit1_start=12510
	slit1_end=7510
	slit1_step=-100
	slit1_ch0=3
	slit1_ch1=0

# 	Log file
	logf=open("table.dat","w")
	logf.write("Energy[kev], TCS_H(mm), TCS_W(mm), Dtheta1[pulse], ESlit1_v, Eslit1_h\n")

##	Energy loop
	for e in energy_list:
	# Moving monochro 
		print e
		stmono.changeE(e)
	# Moving ID
		if e==8.5:
			id.move(7.62)
		else:
			id.moveE(e)
	# energy string
		en_str="%3f"%float(e)
		print en_str

		for tcs_size in tcs_list:
		# string
			tcsstr="%5.3fx%5.3f"%(tcs_size[0],tcs_size[1])

		# Storing axes information
			prefix="%03d_%s"%(f.getNewIdx3(),en_str)
			#tmp=prefix+"_axes.dat"
			#axes.all(tmp)

		# TCS aperture setting
			tcs.setApert(tcs_size[0],tcs_size[1])

		# Tuning dtheta1
			prefix="%03d_%s"%(f.getNewIdx3(),en_str)
			dt1peak=stmono.scanDt1Peak(prefix,dt_start,dt_end,dt_step,dt_main,dt_sub,dt_cnt)

                # Slit1 vertical & horizontal scan
			prefix="%03d"%f.getNewIdx3()
			exs1.fullOpen()

			slit1_vfwhm,slit1_vcenter=exs1.scanV(prefix,slit1_start,slit1_end,slit1_step,slit1_ch0,slit1_ch1,1.0)
			slit1_hfwhm,slit1_hcenter=exs1.scanH(prefix,-slit1_start,-slit1_end,-slit1_step,slit1_ch0,slit1_ch1,0.5)
			exs1.fullOpen()

		# Make log file
#			logf.write("%s,%5.3f,%5.3f,%8.3f,%8.3f,%8.3f,%8.3f\n"%(en_str,tcs_size[0],tcs_size[1],slit1_vcenter,slit1_hcenter,slit2_vcenter,slit2_hcenter))
			#logf.write("%s, %5.3f, %5.3f, %8.1f, %8.3f, %8.3f, %8.3f, %8.3f\n"%(en_str,tcs_size[0],tcs_size[1],dt1peak[1],slit1_vcenter,slit1_hcenter))
	break
	s.close()
