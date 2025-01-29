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
from ExSlit1 import *
from Shutter import *
from ConfigFile import *

while True:
	host = '192.168.163.1'
	port = 10101
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host,port))

##	Device definition
	gonio=Gonio(s)
	mono=Mono(s)
	tcs=TCS(s)
	exs1=ExSlit1(s)
	shutter=Shutter(s)
	conf=ConfigFile()
	f=File("./")

##	Counter channel
	cnt_ch1=3
	cnt_ch2=0
	cnt_ch3=1
	psic=Count(s,1,0)

## 	Gonio Y list
	#ylist=[-17.0728,-17.5728,-18.0728]
	ylist=[1.8550] 	#itumono-needle
	#ylist=[0.8151] 		#itumono-wireitumono-wire 

##	Gonio phi list
	#phi_list=[(0,180),(90,270)]
	phi_list=[(0,180)]

##	Save Gonio position
	sx,sy,sz=gonio.getXYZmm()

	print "START"
## 	Wire scan
	rough_radius=80.0 # [um]
	gstep=1.0 #[um]
	nstep=int(rough_radius/gstep)

       	oname="%03d_scan.dat"%(f.getNewIdx3())
	ofile=open(oname,"w")

       	oname="%03d_brief.dat"%(f.getNewIdx3())
	alldat=open(oname,"w")

	for t in arange(0,1): # number of observations
		# Dtheta1 tune
		prefix="%03d"%f.getNewIdx3()
		fm,fc=mono.scanDt1PeakConfig(prefix,"DTSCAN_NORMAL",tcs)

		# PSIC count
		psic_count=psic.getCount(10.0)[0]/10.0
		psic_pos=psic_count*37/75.0

		# Open shutter
		exs1.openV()
		shutter.open()
		
		for phi_pair in phi_list:
			idx=0
			sx,sy,sz=gonio.getXYZmm()
			for phi in phi_pair:
				gonio.rotatePhi(phi)
				gstep=1.0 # [um]
	
				print "MEASURE LOOP",phi,i
				# PREFIX
				prefix2="phi_%07.2fdeg_%08.4f"%(phi,y)
       				prefix="%03d_%s"%(f.getNewIdx3(),prefix2)
				outfile=prefix+"_gonioV.scn"
	
				# Gonio Z scan range
				print "SCAN STARTED"
				gonio.scanVert2(prefix,-50,50,1,cnt_ch1,cnt_ch2,0.2)
				print "SCAN FINISHED"
	
				# Analyze
				ana=AnalyzePeak(outfile)
				outfig="%s_gonioV.png"%prefix
				comment="GONIO V SCAN"
				fwhm,center=ana.analyzeAll("gonioV[mm]","Intensity",outfig,comment,"OBS","FCEN")
				print "FWRM = %8.5f CENTER=%8.5f "%(fwhm,center)
				no=datetime.datetime.now()
				
				ofile.write("%20s %8.5f %8.3f %10.3f %10.3f\n"%(no,y,phi,fwhm,center))
	
				if idx==0:
					orig=center
				else:
				reve=center
				idx+=1

			## Gonio to saved position
			gonio.moveXYZmm(sx,sy,sz)
			chuten=(orig+reve)/2.0
			zure=chuten-reve
			print "CHUTEN,ZURE",chuten,zure
			gonio.moveUpDown(-zure)

		# Current position
		cx,cy,cz=gonio.getXYZmm()
		# Encoder value
		ex,ey,ez=gonio.getEnc()
		no=datetime.datetime.now()
		alldat.write("%20s %8.3f %6d %8.2f %10.4f%10.4f%10.4f %10.4f%10.4f%10.4f" %
			(no,fm,fc,psic_pos,cx,cy,cz,ex,ey,ez))

		# Sleep
		time.sleep(10)

		for phi_pair in phi_list:
			idx=0
			sx,sy,sz=gonio.getXYZmm()
			for phi in phi_pair:
				gonio.rotatePhi(phi)
				gstep=1.0 # [um]
	
				print "MEASURE LOOP",phi,i
				# PREFIX
				prefix2="phi_%07.2fdeg_%08.4f"%(phi,y)
       				prefix="%03d_%s"%(f.getNewIdx3(),prefix2)
				outfile=prefix+"_gonioV.scn"
	
				# Gonio Z scan range
				print "SCAN STARTED"
				gonio.scanVert2(prefix,-50,50,1,cnt_ch1,cnt_ch2,0.2)
				print "SCAN FINISHED"
	
				# Analyze
				ana=AnalyzePeak(outfile)
				outfig="%s_gonioV.png"%prefix
				comment="GONIO V SCAN"
				fwhm,center=ana.analyzeAll("gonioV[mm]","Intensity",outfig,comment,"OBS","FCEN")
				print "FWRM = %8.5f CENTER=%8.5f "%(fwhm,center)
				no=datetime.datetime.now()
				
				ofile.write("%20s %8.5f %8.3f %10.3f %10.3f\n"%(no,y,phi,fwhm,center))
	
				if idx==0:
					orig=center
				else:
				reve=center
				idx+=1

			## Gonio to saved position
			gonio.moveXYZmm(sx,sy,sz)
			chuten=(orig+reve)/2.0
			zure=chuten-reve
			print "CHUTEN,ZURE",chuten,zure
			gonio.moveUpDown(-zure)

		# Current position
		cx,cy,cz=gonio.getXYZmm()
		# Encoder value
		ex,ey,ez=gonio.getEnc()
		no=datetime.datetime.now()
		alldat.write("%20s %8.3f %6d %8.2f %10.4f%10.4f%10.4f %10.4f%10.4f%10.4f" %
			(no,fm,fc,psic_pos,cx,cy,cz,ex,ey,ez))

	# close shutter
	shutter.close()
	exs1.closeV()

	break
s.close()
