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
from File import *
from FixedPoint import  *
from Att import *
from SPACE import *
from MyException import *
from BM import *
from BS import *
from Stage import *
from Shutter import *
from Capture import *
from Gonio import *
from Colli import *
from Cryo import *
from CenteringNeedle import *
from Zoom import *
from MountPin import *
from Count import *
from FindNeedle import *

class AutoTune:

	def __init__(self,path):
		host = '172.24.242.41'
		port = 10101
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.connect((host,port))

		# Devices
		self.id=ID(self.s)
		self.mono=Mono(self.s)
		self.tcs=TCS(self.s)
		self.f=File(path)
		self.fixedp=FixedPoint(self.s)
		self.att=Att(self.s)
		self.space=SPACE()
		self.bm=BM(self.s)
		self.stage=Stage(self.s)
		self.shutter=Shutter(self.s)
		self.cap=Capture()
		self.colli=Colli(self.s)
		self.bs=BS(self.s)
		self.gonio=Gonio(self.s)
		self.cryo=Cryo(self.s)
		self.zoom=Zoom(self.s)
		
		# current directory
		self.curr_dir=self.f.getAbsolutePath()

	def fixedPoint(self,outfile,total_time):
                of=open(outfile,"w")

                # Fixed point
                starttime=time.time()
                strtime=datetime.datetime.now()
                of.write("#### %s\n"%strtime)
                ttime=0
                counter=Count(self.s,0,1)

                while (ttime <= total_time):
                        currtime=time.time()
                        ttime=currtime-starttime
                        ch1,ch2=counter.getCount(1.0)
                        of.write("12345  %8.3f %12d %12d\n" %(ttime,ch1,ch2))
                        of.flush()

			if ch1<500.0:
				print "Ring may be down\n"
				sys.exit(1)

                strtime=datetime.datetime.now()
                of.write("#### %s\n"%strtime)
                of.close()


	##############
	# dtheta1 tune
	##############
	def dtTune(self):
		try :
			prefix="%s/%03d"%(self.curr_dir,self.f.getNewIdx3())
			self.mono.scanDt1PeakConfig(prefix,"DTSCAN_AUTOTUNE",self.tcs)
	
		except MyException,ttt:
			print "Dtheta1 tune failed."
			print ttt.args[1]
			sys.exit(1)
	##############
	# Changing energy
	##############
	def changeE(self,en):
		# Energy change
    		self.mono.changeE(en)
		# Gap
    		self.id.moveE(en)

	##############
        # Automatic stage tune #
	##############
	def stageTune(self):
                st=StageTune(self.stage,self.cap,self.bm,self.shutter,self.att,self.mono,self.zoom,self.bs,self.cryo)

                # Stage auto tune
                filename="%s/%03d_st_before.ppm"%(self.curr_dir,self.f.getNewIdx3())
                st.doAutomatic(filename)

	##############
	# save pin position
	##############
	def writePinXYZ(self):
		ofile=open("/isilon/users/target/target/Staff/BLtune/pinxyz.dat","a")
		x=self.gonio.getXmm()
		y=self.gonio.getYmm()
		z=self.gonio.getZmm()
		zz=self.gonio.getZZmm()

		date=datetime.datetime.now()
		str="%s %8.4f %8.4f %8.4f %8.4f\n"%(date,x,y,z,zz)

		ofile.write("%s"%str)
		ofile.close()

	##############
	# move pin to saved position
	##############
	def movePreviousXYZ(self):
		ifile=open("/isilon/users/target/target/Staff/BLtune/pinxyz.dat","r")

		lines=ifile.readlines()
		ifile.close()

		final=len(lines)-1

		# Previous centering position
		line=lines[final]
		x=float(line.split()[2])
		y=float(line.split()[3])
		z=float(line.split()[4])
	
		# move gonio
		self.gonio.moveXYZmm(x,y,z)

	#############################################
	# Automatic pin centering  #
	#############################################
	def centerPin(self):
		mp=MountPin(self.space,self.colli,self.bs,self.cryo,self.gonio)
       		mp.mount(4,1)

		self.movePreviousXYZ()

		# Find needle first
		cn=CenteringNeedle(self.gonio,self.cap,self.zoom)
		cn.findNeedle()
		cn.centeringLow()
		cn.centeringHigh()

		self.writePinXYZ()

       		mp.dismount(4,1)

	#############################################
	# All processing
	#############################################
	def doAll(self,energy):
		trayid,pinid=self.space.checkOnGonio()
		if trayid!=0 and pinid!=0:
			print "Dismount your sample first"
			sys.exit(1)

		self.changeE(energy)
		self.dtTune()
		self.stageTune()
		self.centerPin()
    		self.s.close()
		self.cap.disconnect()

	def doPositionOnly(self,energy):
		trayid,pinid=self.space.checkOnGonio()
		if trayid!=0 and pinid!=0:
			print "Dismount your sample first"
			sys.exit(1)
		self.stageTune()
    		self.s.close()

	def doPosition(self,energy):
		trayid,pinid=self.space.checkOnGonio()
		if trayid!=0 and pinid!=0:
			print "Dismount your sample first"
			sys.exit(1)

		self.changeE(energy)
		self.dtTune()
		self.stageTune()
    		self.s.close()

	def doPinCentering(self):
		trayid,pinid=self.space.checkOnGonio()
		if trayid!=0 and pinid!=0:
			print "Dismount your sample first"
			sys.exit(1)
		self.centerPin()
    		self.s.close()

	def doPinCenterOnly(self):
		self.movePreviousXYZ()
		# Find needle first
		cn=CenteringNeedle(self.gonio,self.cap,self.zoom)
		cn.findNeedle()
		cn.centeringLow()
		cn.centeringHigh()
		self.writePinXYZ()

	def doFixedRecover(self,energy):
		for i in range(0,12):
			file="%02d_fixed.scn"%i
			self.changeE(energy)
			self.dtTune()
			self.stageTune()
			self.fixedPoint(file,3600)

if __name__=="__main__":

	at=AutoTune(sys.argv[2])
	en=float(sys.argv[1])

	#at.doAll(en)

	#at.doPinCenterOnly()
	at.doPosition(en)
	#at.doPositionOnly(en)
