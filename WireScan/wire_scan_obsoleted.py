#!/bin/env python 
import sys
import socket
import time
import datetime

# My library
from ID import *
from TCS import *
from AxesInfo import *
from File import *
from Mono import *
from Gonio import *
from Count import *


host = '172.24.242.41'
port = 10101
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))

while True:
	print "Input index [example. 00, 01,...]:"
 
#	energy_list=[8.5,9.0,12.398,15.0,18.0,20.0]
#	tcs_list=[(0.026,0.04),(0.1,0.1),(0.2,0.2),(0.3,0.3),(0.4,0.4),(0.5,0.5)]
#	energy_list=[8.5,12.398,18.0]

	energy_list=[12.398]
	#tcs_list=[(0.026,0.04),(0.1,0.1),(0.3,0.3),(0.5,0.5)]
	tcs_list=[(0.1,0.1)]

# Constructer
	stmono=Mono(s)
	tcs=TCS(s)
	id=ID(s)
	axes=AxesInfo(s)
	f=File("./")
	gonio=Gonio(s)

# Counter <-> channel
	ic=3	# I0
	pin3=0	# pin photodiode after sample

# Gonio scan parameters
	gmain=pin3
	gsub=ic
	vscan_position=133641 # gonio Y position @ Z scan
	hscan_position=-1487 # gonio Z position @ Y scan

	y1start=131880	# pulse(1um/10pls)  (sense=-1)
	y1end=131630	# pulse(1um/10pls)  (sense=-1)

	z1start=-289.0	# um
	z1end=-259.0	# um
	step1=0.2	# um

### Fixed point setting
##	Energy loop
	for e in energy_list:
	# Moving monochro 
		stmono.changeE(e)
	# Moving ID
		if e==8.5:
			id.move(7.62)
		else:
			id.moveE(e)
	# energy string
		en_str="%3f"%float(e)

		for tcs_size in tcs_list:
		# string
			tcsstr="%5.3fx%5.3f"%(tcs_size[0],tcs_size[1])
		# TCS aperture setting
			#tcs.setApert(tcs_size[0],tcs_size[1])
		# Tuning dtheta1
			#prefix="%03d_%s"%(f.getNewIdx3(),en_str)
			#dt1peak=stmono.scanDt1PeakConfig(prefix,"DTSCAN_AUTOTUNE",tcs)

		##############
		# Wire Z scan
		##############
			prefix="%03d_%s"%(f.getNewIdx3(),en_str)
			gonio.moveY(vscan_position)
			#final_z=gonio.scanZ(prefix,z1start,z1end,step1,gmain,gsub,0.2)
			final_z=gonio.scanZenc(prefix,z1start,z1end,step1,gmain,gsub,0.2)
			print final_z
			z_peak1=final_z[1]/10.0

			sys.exit(1)

		##############
		# Wire Y scan
		##############
			prefix="%03d_%s"%(f.getNewIdx3(),en_str)
			gonio.moveZ(hscan_position)
			final_y=gonio.scanY(prefix,y1start,y1end,y1step,gmain,gsub,0.2)
			y_peak1=-final_y[1]/10.0


		# Make log file
			logfile.write("%s, %5.3f, %5.3f, %8.1f, %8.3f, %8.3f,%8.3f,%8.3f, %8.3f, %8.3f\n"%(en_str,tcs_size[0],tcs_size[1],dt1peak[1],z_peak1,y_peak1,z_peak2,y_peak2,diffz_peak,diffy_peak))
	break
	s.close()
