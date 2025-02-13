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
		#host = '192.168.163.1'
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
		#self.space=SPACE()
		self.bm=BM(self.s)
		self.stage=Stage(self.s)
		self.shutter=Shutter(self.s)
		self.cap=Capture()
		self.colli=Colli(self.s)
		self.bs=BS(self.s)
		self.gonio=Gonio(self.s)
		self.cryo=Cryo(self.s)
		self.zoom=Zoom(self.s)
		self.slit1=ExSlit1(self.s)
		
		# current directory
		self.curr_dir=self.f.getAbsolutePath()
		print self.curr_dir

	def fixedPoint(self,outfile,total_time,ch1,ch2):
                of=open(outfile,"w")

                # Fixed point
                starttime=time.time()
                strtime=datetime.datetime.now()
                of.write("#### %s\n"%strtime)
                ttime=0
                counter=Count(self.s,ch1,ch2)

		################################
		################################
		################################
		# if you use pin at sample
		# CHECK THE DETECTOR COVER
		################################
		################################
		################################
		self.shutter.open()

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
		try:
			prefix="%s/%03d"%(self.curr_dir,self.f.getNewIdx3())
			self.mono.scanDt1PeakConfig(prefix,"DTSCAN_AUTOTUNE",self.tcs)
	
		except MyException,ttt:
			comment="Dtheta1 tune failed. Check DSS/Ring current."
			raise MyException("%s: %s\n"%(comment,ttt.args[0]))
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
		# Stage tune class
                st=StageTune(self.tcs,self.stage,self.cap,self.bm,self.shutter,self.att,self.mono,self.zoom,self.bs,self.cryo)

		# Ex Slit1 open
		self.slit1.openV()

                # Stage auto tune
                prefix="%s/%03d_st_before"%(self.curr_dir,self.f.getNewIdx3())
                st.doAutomatic(prefix)

		# Ex Slit1 open
		self.slit1.closeV()


	##############
	# save pin position
	##############
	def writePinXYZ(self):
		ofile=open("/isilon/BL32XU/BLtune/pinxyz.dat","a")
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
		ifile=open("/isilon/BL32XU/BLtune/pinxyz.dat","r")

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

	def prepExp(self):
		# Ex Slit1 close
		self.slit1.closeV()
		# Shutter close
		self.shutter.close()
		# Collimator evacuation
		self.colli.go(-20000)
		# Cryo ON
		self.cryo.goOff()
		# BS Off
		self.bs.goOff()
		# BM off
		self.bm.go(-75000)

	def doPositionOnly(self):
		# Collimator evacuation
		self.colli.goOff()

		# Current TCS aperture 
		tcsh,tcsw=self.tcs.getApert()
		print "TCS aperture saved"

		# set TC slit aperture to 0.1 x 0.1 mm
		print "TCS is set to 0.1x0.1mm"
		self.tcs.setApert(0.1,0.1)
	
		# Gonio moving
		curr_x,curr_y,curr_z=self.gonio.getXYZmm()

		if curr_y<0.0:
			newy=curr_y+20.0
			self.gonio.moveXYZmm(curr_x,newy,curr_z)

		time.sleep(20)

		# dtheta1 tune
		try:
			self.dtTune()
		except MyException,ttt:
			raise MyException(ttt.args[0])
		try :
			self.stageTune()
	
		except MyException,ttt:
                        raise MyException("Stage auto tune failed:%s"%ttt.args[0])

		# reset gonio Position
		self.gonio.moveXYZmm(curr_x,curr_y,curr_z)

		# Set TCS aperture to the original value
		self.tcs.setApert(tcsh,tcsw)

    		self.s.close()

	def doPosition(self):
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
		#self.movePreviousXYZ()
		# Find needle first
		cn=CenteringNeedle(self.gonio,self.cap,self.zoom)
		#cn.findNeedle()
		cn.centeringLow()
		cn.centeringHigh()
		self.writePinXYZ()

	def doFixedRecover(self,time,energy,ch1,ch2):
		for i in range(0,time):
			file="%02d_fixed.scn"%i
			self.changeE(energy)
			self.dtTune()
			self.stageTune()
			self.fixedPoint(file,3600,ch1,ch2)

if __name__=="__main__":

	at=AutoTune("./")
	#en=float(sys.argv[1])

	if len(sys.argv)>1:
		print "No need for inputing arguments."

	ch1=3 # ion chamber
	ch2=0 # pin at sample

	#at.doFixedRecover(24,en,ch1,ch2)
	#at.doAll(en)
	#at.doPinCenterOnly()
	#at.doPosition()
	at.doPositionOnly()
	#at.prepExp()
