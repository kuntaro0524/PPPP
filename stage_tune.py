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
from ExSlit2 import *
from Capture import *
from Monitor import *
from Count import *


host = '172.24.242.41'
port = 10101
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))

while True:

# Constructer
	stmono=Mono(s)
	tcs=TCS(s)
	id=ID(s)
	axes=AxesInfo(s)
	f=File("./")
	exs1=ExSlit1(s)
	exs2=ExSlit2(s)
        cap=Capture()
	moni=Monitor(s)


# Counter <-> channel
	ic=0	# I0
	pin1=1	# Pin photodiode in chamber at upstream
	pin2=2	# Pin photodiode in chamber at downstream 
	pin3=3	# pin photodiode after sample

# TCS apearture
	tcs_size=(0.1,0.1)

# Dtheta1 tune parameters
	dt_start=-88000
	dt_end=-83000
	dt_step=20
	dt_cnt=0.2
	dt_main=pin3
	dt_sub=ic

# St2Slit1 knife edge scan
	slit1_start=18010
	slit1_end=10
	slit1_step=-50
	slit1_ch0=3
	slit1_ch1=0

# St2Slit2 knife edge scan
	slit2_start=8000
	slit2_end=-1500
	slit2_step=-50
	slit2_ch0=3
	slit2_ch1=0

# Stage knife edge scan
	slit2_upper_pos=124
	slit2_ring_pos=1353
	st-z_start=8000
	st-z_end=-1500
	st-y_start=8000
	st-y_end=-1500
	state_step=-50
	stage_ch0=3
	staget_ch1=0

# 	Log file
	logf=open("table.dat","w")
	logf.write("Energy[kev], Dtheta1[pulse], Ty1[pulse], ESlit1_v, Eslit1_h, ESlit2_v, Eslit2, St-y, St-z, IC0, Pin3, Pin4, Pin6\n")

    while (ttmie <= total_time):

		# Storing axes information
			prefix="%03d_%s"%(f.getNewIdx3(),en_str)
			tmp=prefix+"_axes.dat"
			axes.all(tmp)

		# TCS aperture setting
			tcs.setApert(tcs_size[0],tcs_size[1])

	## before tuning
		# Scintillator Monitor On
			moni.on()
		# Capture Image before Tuning
			cap.unsetCross()
	                cap.capture(ofile)
			cap.setCross()
		# Scintillator Monitor Off
			moni.off()

                # Slit1 vertical & horizontal scan
			prefix="%03d"%f.getNewIdx3()
			exs1.fullOpen()

			slit1_vfwhm,slit1_vcenter=exs1.scanV(prefix,slit1_start,slit1_end,slit1_step,slit1_ch0,slit1_ch1,1.0)
			slit1_hfwhm,slit1_hcenter=exs1.scanH(prefix,-slit1_start,-slit1_end,-slit1_step,slit1_ch0,slit1_ch1,0.5)
			exs1.fullOpen()

                # Slit2 vertical & horizontal scan
			prefix="%03d"%f.getNewIdx3()
			exs2.fullOpen()

			slit2_vfwhm,slit2_vcenter=exs2.scanV(prefix,slit2_start,slit2_end,slit2_step,slit2_ch0,slit2_ch1,1.0)
			slit2_hfwhm,slit2_hcenter=exs2.scanH(prefix,-slit2_start,-slit2_end,-slit2_step,slit2_ch0,slit2_ch1,0.5)
			exs2.fullOpen()

##			logf.write("Dtheta1[pulse], ESlit1_v, Eslit1_h, ESlit2_v, Eslit2, St-y, St-z, IC0, Pin3, Pin4, Pin6\n")
			logf.write("%8.3f, %8.3f, %8.3f, %8.3f, %8.3f, %8.3f, %8.3f, %12d, %12d, %12d, %12d\n"%(dt1peak, slit1_vcenter, slit1_hcenter, slit2_vcenter, slit2_hcenter, stage-y_center, stage-z_center, ch0, ch1, ch2, ch3))


	## dtheta tuning

		# Tuning dtheta1
			prefix="%03d_%s"%(f.getNewIdx3(),en_str)
			dt1peak=stmono.scanDt1Peak(prefix,dt_start,dt_end,dt_step,dt_main,dt_sub,dt_cnt)

                # Slit1 vertical & horizontal scan
			prefix="%03d"%f.getNewIdx3()
			exs1.fullOpen()

			slit1_vfwhm,slit1_vcenter=exs1.scanV(prefix,slit1_start,slit1_end,slit1_step,slit1_ch0,slit1_ch1,1.0)
			slit1_hfwhm,slit1_hcenter=exs1.scanH(prefix,-slit1_start,-slit1_end,-slit1_step,slit1_ch0,slit1_ch1,0.5)
			exs1.fullOpen()

                # Slit2 vertical & horizontal scan
			prefix="%03d"%f.getNewIdx3()
			exs2.fullOpen()

			slit2_vfwhm,slit2_vcenter=exs2.scanV(prefix,slit2_start,slit2_end,slit2_step,slit2_ch0,slit2_ch1,1.0)
			slit2_hfwhm,slit2_hcenter=exs2.scanH(prefix,-slit2_start,-slit2_end,-slit2_step,slit2_ch0,slit2_ch1,0.5)
			exs2.fullOpen()

		# Scintillator Monitor On
			moni.on()
		# Capture Image before Tuning
			cap.unsetCross()
	                cap.capture(ofile)
			cap.setCross()
		# Scintillator Monitor Off
			moni.off()

		# Make log file
##			logf.write("Dtheta1[pulse], ESlit1_v, Eslit1_h, ESlit2_v, Eslit2, St-y, St-z, IC0, Pin3, Pin4, Pin6\n")
			logf.write("%8.3f, %8.3f, %8.3f, %8.3f, %8.3f, %8.3f, %8.3f, %12d, %12d, %12d, %12d\n"%(dt1peak, slit1_vcenter, slit1_hcenter, slit2_vcenter, slit2_hcenter, stage-y_center, stage-z_center, ch0, ch1, ch2, ch3))

	# Tuning by Stage

		# Slit2 set to tuning position


                # Slit2 vertical & horizontal scan
			prefix="%03d"%f.getNewIdx3()
			exs2.fullOpen()

			slit2_vfwhm,slit2_vcenter=exs2.scanV(prefix,slit2_start,slit2_end,slit2_step,slit2_ch0,slit2_ch1,1.0)
			slit2_hfwhm,slit2_hcenter=exs2.scanH(prefix,-slit2_start,-slit2_end,-slit2_step,slit2_ch0,slit2_ch1,0.5)
			exs2.fullOpen()

		# Scintillator Monitor On
			moni.on()
		# Capture Image before Tuning
			cap.unsetCross()
	                cap.capture(ofile)
			cap.setCross()
		# Scintillator Monitor Off
			moni.off()

	break
	s.close()
