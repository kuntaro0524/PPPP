#!/bin/env python 
import sys
import socket
import time
import math
from pylab import *

# My library
from Gonio import *
from ID import *
from Mono import *
from TCS import *
from ConfigFile import *
from Count import *

# Coded by K.Hirata
# please see 140527 - 140528 experiments

while True:
	#host = '192.168.163.1'
	host = '172.24.242.41'
	port = 10101
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host,port))

##	Device definition
	gonio=Gonio(s)
	conf=ConfigFile()
	f=File("./")

##	Counter channel
	cnt_ch1=3
	cnt_ch2=1 #PSIC
	counter=Count(s,cnt_ch1,cnt_ch2)

##	Gonio phi list
	phi_list=[(0,180),(90,270)]

##	Save Gonio position
	sx,sy,sz=gonio.getXYZmm()

## 	Wire scan
	rough_radius=80.0 # [um]
	gstep=1.0 #[um]
	nstep=int(rough_radius/gstep)

       	oname="%03d_scan.dat"%(f.getNewIdx3())
	ofile=open(oname,"w")
       	oname="%03d_result.dat"%(f.getNewIdx3())
	sfile=open(oname,"w")

	while(1):
		finish_flag=0
		for phi_pair in phi_list:
			idx=0
			ox,oy,oz=gonio.getXYZmm()
			for phi in phi_pair:
				gonio.rotatePhi(phi)
				gstep=1.0 # [um]
		
				print "Scan at rotation=",phi,"[deg.]"
				# PREFIX
				prefix2="phi_%07.2fdeg_%08.4f"%(phi,sy)
       				prefix="%03d_%s"%(f.getNewIdx3(),prefix2)
				outfile=prefix+"_gonioV.scn"
		
				# Gonio Z scan range
				print "Scan STARTED"
				gonio.scanVert2(prefix,-50,50,1,cnt_ch1,cnt_ch2,0.1)
				print "Scan FINISHED"
		
				# Analyze
				ana=AnalyzePeak(outfile)
				outfig="%s_gonioV.png"%prefix
				comment="GONIO V SCAN"
				fwhm,center=ana.analyzeAll("gonioV[mm]","Intensity",outfig,comment,"OBS","FCEN")
				print "Needle shade FWHM = %8.5f[um] CENTER=%8.5f[um]"%(fwhm,center)
	
				# Encoder value
				x,y,z=gonio.getXYZmm()
				ex,ey,ez=gonio.getEnc()
	
				ofile.write("%8.3f %10.3f %8.3f %10.5f%10.5f%10.5f%10.5f%10.5f%10.5f\n"
					%(fwhm,center,phi,x,y,z,ex,ey,ez))
				ofile.flush()
		
				if idx==0:
					orig=center
				else:
					reve=center
				idx+=1
	
			## Gonio to saved position
			gonio.moveXYZmm(ox,oy,oz)
			chuten=(orig+reve)/2.0
			zure=chuten-reve
			print "CHUTEN,ZURE",chuten,zure
			gonio.moveUpDown(-zure)
	
			x,y,z=gonio.getXYZmm()
			ex,ey,ez=gonio.getEnc()
			no=datetime.datetime.now()
	
			# PSIC
			itime=10.0
			psic=int(counter.getCount(itime)[1])
			psic_pos=psic/100.0/itime*37/75 #[um]

			sfile.write("%20s %10.5f%10.5f%10.5f%10.5f%10.5f%10.5f %10.5f%10.2f%10.5f\n"
				%(no,x,y,z,ex,ey,ez,chuten,psic_pos,zure))
			sfile.flush()

			# is finished?
			if math.fabs(zure)<0.5:
				finish_flag+=1
			if finish_flag==2:
				break
		if finish_flag==2:
			break
	if finish_flag==2:
		ofile.close()
		sfile.close()
		break
s.close()

