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
from Gonio import *

host = '172.24.242.41'
port = 10101
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))

while True:
	print "Input index [example. 00, 01,...]:"
 
	energy_list=[8.5,9.0,12.398,15.0,18.0,20.0]
	tcs_list=[(0.1,0.1),(0.2,0.2),(0.3,0.3),(0.4,0.4),(0.5,0.5)]

# Constructer
	stmono=Mono(s)
	tcs=TCS(s)
	id=ID(s)
	axes=AxesInfo(s)
	f=File("./")
	gonio=Gonio(s)

# Counter <-> channel
	ic=0	# I0
	pin2=2	# Pin photodiode in chamber
	pin3=3	# pin photodiode after sample

# Dtheta1 tune parameters
	dt_start=-92000
	dt_end=-86000
	dt_step=20
	dt_cnt=0.2
	dt_main=pin2
	dt_sub=ic

# Gonio scan parameters
	gmain=pin3
	gsub=ic
	vscan_position=149501 # gonio Y position @ Z scan
	hscan_position=8288 # gonio Z position @ Y scan

	y1start=149500	# pulse(1um/10pls)  (sense=-1)
	y1end=152000	# pulse(1um/10pls)  (sense=-1)

	z1start=7400	# pulse(1um/10pls)
	z1end=10500	# pulse(1um/10pls)
	step1=100	# pulse(1um/10pls)

# 	Log file
	logfile=open("table.dat","w")

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
			prefix="%02d_%s"%(f.getNewIdx2(),en_str)
			tmp=prefix+"_axes.dat"
			axes.all(tmp)
		# TCS aperture setting
			tcs.setApert(tcs_size[0],tcs_size[1])
		# Tuning dtheta1
			prefix="%02d_%s"%(f.getNewIdx2(),en_str)
			dt1peak=stmono.scanDt1Peak(prefix,dt_start,dt_end,dt_step,dt_main,dt_sub,dt_cnt)

		#############
		# 2D wire scan
                # gonio vertical scan
		##############
		# Wire Z scan
		##############
			prefix="%02d_%s"%(f.getNewIdx2(),en_str)
			gonio.moveY(vscan_position)
			next_center=gonio.scanZ(prefix,z1start,z1end,step1,gmain,gsub,0.2)
			
			z2start=next_center-200
			z2end=next_center+200
			z2step=2

			prefix="%02d"%f.getNewIdx2()
			final_z=gonio.scanZ(prefix,z2start,z2end,2,gmain,gsub,1.0)
			z_peak=final_z/10.0

		##############
		# Wire Y scan
		##############
			prefix="%02d"%f.getNewIdx2()
			gonio.moveZ(hscan_position)
			next_center=gonio.scanY(prefix,y1start,y1end,step1,gmain,gsub,0.2)
			
			y2start=next_center-200
			y2end=next_center+200
			y2step=2

			prefix="%02d"%f.getNewIdx2()
			final_y=gonio.scanY(prefix,y2start,y2end,2,gmain,gsub,0.5)
			y_peak=-final_y/10.0

		# Make log file
			logfile.write("%s,%5.3f,%5.3f,%8.1f,%8.3f,%8.3f\n"%(en_str,tcs_size[0],tcs_size[1],dt1peak,z_peak,y_peak))
	break
	s.close()
