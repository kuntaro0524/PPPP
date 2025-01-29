#!/bin/env python 
import sys
import socket
import time
import os

# My library
from ID import *
from TCS import *
from AxesInfo import *
from File import *
from Mono import *
from ExSlit1 import *
from ExSlit2 import *

host = '172.24.242.41'
port = 10101
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))

while True:
	print "Type: slit1/slit2/both"
	msg = raw_input()

	print msg

	if msg!="slit1" and msg!="slit2" and msg!="both":
		print "Input correct option."
		sys.exit(1)

	energy_list=[12.728] # 100628 hashi WaveLength = 0.9741 ang
	tcs_list=[(0.1,0.1)]

# Constructer
	stmono=Mono(s)
	tcs=TCS(s)
	id=ID(s)
	axes=AxesInfo(s)
	f=File("./")
	exs1=ExSlit1(s)
	exs2=ExSlit2(s)


# Counter <-> channel
	ic=0	# I0
	pin2=2	# Pin photodiode in chamber
	pin3=3	# pin photodiode after sample

# Dtheta1 tune parameters
	dt_start=conf.getCondition2("DTSCAN","start")
	dt_end=conf.getCondition2("DTSCAN","end")
	dt_step=conf.getCondition2("DTSCAN","step")
	dt_cnt=conf.getCondition2("DTSCAN","time")
	dt_main=conf.getCondition2("DTSCAN","ch1")
	dt_sub=conf.getCondition2("DTSCAN","ch2")

# St2Slit1 knife edge scan
	slit1_upper_start=conf.getCondition2("SLIT1","upper_start")
	slit1_upper_end=conf.getCondition2("SLIT1","upper_end")
	slit1_ring_start=conf.getCondition2("SLIT1","ring_start")
	slit1_ring_end=conf.getCondition2("SLIT1","ring_end")
	slit1_step=conf.getCondition2("SLIT1","step")
	slit1_ch0=conf.getCondition2("SLIT1","ch0")
	slit1_ch1=conf.getCondition2("SLIT1","ch1")

##########################

# St2Slit2 knife edge scan
	slit2_start=conf.getCondition2("SLIT2","start")
	slit2_end=conf.getCondition2("SLIT2","end")
	slit2_step=conf.getCondition2("SLIT2","step")
	slit2_ch0=conf.getCondition2("SLIT2","ch0")
	slit2_ch1=conf.getCondition2("SLIT2","ch1")

# 	Log file
	logf=open("table.dat","w")
	logf.write("Energy[kev], TCS_H(mm), TCS_W(mm), Dtheta1[pulse], ESlit1_v, Eslit1_h, ESlit2_v, Eslit2\n")


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
			tmp=prefix+"_axes.dat"
			axes.all(tmp)

		# TCS aperture setting
			tcs.setApert(tcs_size[0],tcs_size[1])

		# Tuning dtheta1
			prefix="%03d_%s"%(f.getNewIdx3(),en_str)
			dt1peak=stmono.scanDt1Peak(prefix,dt_start,dt_end,dt_step,dt_main,dt_sub,dt_cnt)

                # Slit1 vertical & horizontal scan
                        if msg=="slit1" or msg=="both":
				print "slit1 scan"
	                        prefix="%03d"%f.getNewIdx3()
        	                exs1.fullOpen()

	               	        slit1_vfwhm,slit1_vcenter=exs1.scanV(prefix,slit1_upper_start,slit1_upper_end,slit1_step,slit1_ch0,slit1_ch1,0.5)
                        	slit1_hfwhm,slit1_hcenter=exs1.scanH(prefix,slit1_ring_start,slit1_ring_end,slit1_step,slit1_ch0,slit1_ch1,1.0)
	                        exs1.fullOpen()

                # Slit2 vertical & horizontal scan
			if msg=="slit2" or msg=="both":
				print "slit2 scan"
				prefix="%03d"%f.getNewIdx3()
				exs2.fullOpen()

#####                        	slit2_vfwhm,slit2_vcenter=exs2.scanV(prefix,slit2_start,slit2_end,slit2_step,slit2_ch0,slit2_ch1,0.5)
                        	slit2_hfwhm,slit2_hcenter=exs2.scanH(prefix,-slit2_start,-slit2_end,-slit2_step,slit2_ch0,slit2_ch1,1.0)
                        	exs2.fullOpen()

		# Make log file
			print "output file"
			if msg=="slit1":
				logf.write("%s,%5.3f,%5.3f,%8.3f,%8.3f\n"%(en_str,tcs_size[0],tcs_size[1],slit1_vcenter,slit1_hcenter))
			if msg=="slit2":
                                logf.write("%s,%5.3f,%5.3f,%8.3f,%8.3f\n"%(en_str,tcs_size[0],tcs_size[1],slit2_vcenter,slit2_hcenter))
			if msg=="both":
				logf.write("%s, %5.3f, %5.3f, %8.1f, %8.3f, %8.3f, %8.3f, %8.3f\n"%(en_str,tcs_size[0],tcs_size[1],dt1peak[1],slit1_vcenter,slit1_hcenter,slit2_vcenter,slit2_hcenter))
#        print "Continue ?"
#	print "Type: Yes/No"
#        msg2 = raw_input()
#        print msg2
#        if msg2=="No":
	break
	s.close()
print "finished"
