#!/bin/env python
import sys
import socket
import time
import datetime

from numpy import *

# My library
from File import *
from ExSlit2 import *
from TCS import *
from BM import *
from Capture import *
from Count import *
from Mono import *
from ConfigFile import *
from Att import *
from BeamCenter import *
from Stage import *
from StageTune import *
from Zoom import *
from BS import *
from Shutter import *
from Cryo import *
from ID import *
from ExSlit1 import *
from Light import *
from Count import *
from AnalyzePeak import *
from Gonio import *
from Colli import *
from Cover import *
from CCDlen import *

class Procedure:
	def __init__(self,server):
		self.s=server
		self.isInit=False

	def readConfig(self):
		conf=ConfigFile()
		# Reading config file
        	try :
		## Dtheta 1
                	self.scan_dt1_ch1=int(conf.getCondition2("DTSCAN","ch1"))
                	self.scan_dt1_ch2=int(conf.getCondition2("DTSCAN","ch2"))
			self.scan_dt1_start=int(conf.getCondition2("DTSCAN","start"))
			self.scan_dt1_end=int(conf.getCondition2("DTSCAN","end"))
			self.scan_dt1_step=int(conf.getCondition2("DTSCAN","step"))
			self.scan_dt1_time=conf.getCondition2("DTSCAN","time")

		## Fixed point parameters
                	self.fixed_ch1=int(conf.getCondition2("FIXED_POINT","ch1"))
                	self.fixed_ch2=int(conf.getCondition2("FIXED_POINT","ch2"))
			self.block_time=conf.getCondition2("FIXED_POINT","block_time")
			self.total_num=conf.getCondition2("FIXED_POINT","total_num")
			self.count_time=conf.getCondition2("FIXED_POINT","time")

        	except MyException,ttt:
                	print ttt.args[0]
                	print "Check your config file carefully.\n"
                	sys.exit(1)

	def init(self):
		# settings
		self.mono=Mono(self.s)
		self.tcs=TCS(self.s)
		self.bm=BM(self.s)
       		self.f=File("./")
		self.cap=Capture()
		self.slit2=ExSlit2(self.s)
		self.slit1=ExSlit1(self.s)
        	self.att=Att(self.s)
        	self.stage=Stage(self.s)
        	self.zoom=Zoom(self.s)
        	self.bs=BS(self.s)
		self.shutter=Shutter(self.s)
		self.cryo=Cryo(self.s)
		self.id=ID(self.s)
		self.light=Light(self.s)
		self.gonio=Gonio(self.s)
		self.colli=Colli(self.s)
		self.isInit=True

	def setAtt(self,thick):
		if self.isInit==False:
			self.init()
		self.att.setAtt(thick)

        def calcAttFac(self,wl,thickness):
		self.att.calcAttFac(wl,thickness)

	def prepScan(self):
		self.openShutters()

	def openShutters(self):
		if self.isInit==False:
			self.init()
		self.slit1.openV()
		self.light.off()
		self.shutter.open()

	def closeShutters(self):
		if self.isInit==False:
			self.init()
		self.shutter.close()
		self.slit1.closeV()

	def prepView(self):
		if self.isInit==False:
			self.init()
		self.closeShutters()
        	self.light.on()

	def openShutter(self):
        	self.slit1.openV()
        	self.light.off()
        	self.shutter.open()

	def finishScan(self):
		self.slit1.closeV()
		self.shutter.close()

	def moveGonioXYZ(self,x,y,z):
		self.gonio.moveXYZmm(x,y,z)

	def scanStageYwire(self,prefix):
		save_sty=self.stage.getY()

        	#self.stage.scanYwire(prefix,step_mm,num_half,ch1,ch2,time):

        	self.stage.scanYneedle(prefix,0.001,200,3,0,0.2)

		# Move to the origin
		self.stage.moveY(save_sty)

	def scanStageZwire(self,prefix):
		save_stz=self.stage.getZ()
        	self.stage.scanZneedle(prefix,0.001,200,3,0,0.2)
		# Move to the origin
		self.stage.moveZ(save_stz)

	def tuneStageZneedle(self,prefix):
		self.openShutters()
       		stz_fwhm,stz_cen=self.stage.scanZneedleMove(prefix,0.002,40,3,0,0.2) #prefix,step,num_half,ch1,ch2,time
		#stz_fwhm=9999
		#stz_cen=8888

		# StageY scan and Move
		self.gonio.moveXYZmm(nsx,nsy,nsz)
       		prefix="%03d"%self.f.getNewIdx3()
       		self.stage.scanYneedle(prefix,0.001,20,3,0,1.0)
		datfile="%s_stagey.scn"%prefix
		ycenter=self.analyzeKnife(datfile)

	def makePikaTable(self,energy_list):
		# Initialization
		if self.isInit==False:
			self.init()

		# Output file
		ofile=open("pika.tbl","w")

		# Needle for stageZ tune
		nx=  0.1135
		ny=-13.7741
		nz=  0.5709

		## needle saki centered
		nsx=  0.1145
		nsy=-13.7441
		nsz=  0.5709

		## needle Evacuated position gonioY
		ney=  ny+12.0

		########
		# Main loop
		########
		for en in energy_list:
			## capture
			self.finishCapture()
			self.closeShutters()
			self.setAtt(0.0)

			# Energy change
			curr_dt1,junk=self.changeEandTune(en)
			#curr_dt1=9922

			# StageZ scan and Move
        		prefix="%03d"%self.f.getNewIdx3()
			self.gonio.moveXYZmm(nsx,nsy,nsz)

			self.prepView()

			### averaging center x,y
        		prefix="%03d"%self.f.getNewIdx3()
			path=os.path.abspath("./")
			capfile="%s/%s_needle.png"%(path,prefix)
        		self.cap.captureWithCross(capfile,bright=15)

			# wait for thermal equillibrium
			time.sleep(60)
			self.gonio.moveXYZmm(nx,ny,nz)
			self.openShutters()
        		stz_fwhm,stz_cen=self.stage.scanZneedleMove(prefix,0.002,40,3,0,0.2) #prefix,step,num_half,ch1,ch2,time
			#stz_fwhm=9999
			#stz_cen=8888

			# StageY scan and Move
			self.gonio.moveXYZmm(nsx,nsy,nsz)
        		prefix="%03d"%self.f.getNewIdx3()
        		self.stage.scanYneedle(prefix,0.001,20,3,0,1.0)
			datfile="%s_stagey.scn"%prefix
			ycenter=self.analyzeKnife(datfile)
			self.stage.setYmm(ycenter)
			#ycenter=9999

			# Pika	
			# 2% transmission
			wave=12.3984/en
			trans=0.02
			self.att.setAttTrans(wave,trans)
			# Capture preparation
        		capfile="%03d_capture"%self.f.getNewIdx3()
			self.gonio.moveXYZmm(nsx,ney,nsz)
			self.prepCapture()
			capx,capy=self.captureBM(capfile)

			# Capture finished => logfile
			self.finishCapture()
			self.closeShutters()
			ofile.write("%8.5f %5d %10.5f %10.5f %8.2f %8.2f\n"%(en,curr_dt1,stz_cen,ycenter,capx,capy))
			ofile.flush()

		ofile.close()

	def analyzeKnife(self,datfile):

                ana=AnalyzePeak(datfile)
                xdat,ydat,junk=ana.prepData3(1,2,1)
                dx,dy=ana.derivative(xdat,ydat)

                dxx=numpy.array(dx)
                dyy=numpy.array(dy)

                min_idx=dyy.argmin()

                start=min_idx-5
                end=min_idx+5

                #for idx in range(0,len(dxx)):
                        #print 1234,dxx[idx],dyy[idx],1234

                sum=0.0
                sum_x=0.0
                for idx in range(start,end):
                        #print idx,dxx[idx],dyy[idx]
                        sum+=dxx[idx]*dyy[idx]
                        sum_x+=dyy[idx]
                center=sum/sum_x

		return center

	def makeTable(self,energy):
		if self.isInit==False:
			self.init()
		## PRE-PREFIX
		prefix="%03d_%08.4fkeV"%(self.f.getNewIdx3(),energy)
		oname="%s.dat"%prefix
		ofile=open(oname,"w")

		## needle z tune
		nx=  0.1135
		ny=-13.7741
		nz=  0.5709
		evac_y=ny+1.0

		## needle saki centered
		nsx=  0.1145
		nsy=-13.7441
		nsz=  0.5709

		# Counter channel
		cnt1=3
		cnt2=0
		counter=Count(self.s,cnt1,cnt2)

		## Energy change
		self.changeE(energy)
		self.gonio.moveXYZmm(nx,ny,nz)
		self.colli.off()

		## Dtheta1 tune
		prefix="%03d"%(self.f.getNewIdx3())
                #if energy<=10.0:
                        #time.sleep(600)
                if energy > 10.0:
                        prefix="%03d"%(self.f.getNewIdx3())
                        dt1_fwhm,dt1_peak=self.mono.scanDt1PeakConfig(prefix,"DTSCAN_NORMAL",self.tcs)
                elif energy <= 10.0:
                        prefix="%03d"%(self.f.getNewIdx3())
                        dt1_fwhm,dt1_peak=self.mono.scanDt1PeakConfig(prefix,"DTSCAN_LOWENERGY",self.tcs)

		# Needle on for scan table Z
		self.gonio.moveXYZmm(nx,ny,nz)
		
		# StageZ scan
        	prefix="%03d"%self.f.getNewIdx3()
        	stz_fwhm,stz_cen=self.stage.scanZneedleMove(prefix,0.002,40,3,0,0.2) #prefix,step,num_half,ch1,ch2,time
		
		# Stage Y scan
		#print "Stage Y scan starts"
		#print "START",self.stage.getY()
		#self.gonio.moveXYZmm(nsx,nsy,nsz)

        	#prefix="%03d"%self.f.getNewIdx3()
        	#self.stage.scanYneedle(prefix,0.001,20,3,0,1.0)
 		#print "Stage Y scan ends"
		#print "End",self.stage.getY()

		# Evacuate gonio Y
		self.gonio.moveXYZmm(nx,evac_y,nz)

		# Collimator scan
        	prefix="%03d"%self.f.getNewIdx3()
		col_y,col_z,col_fwhmz,col_fwhmy=self.colli.scanWithoutPreset(prefix,3,0.05)

		cnt_str=counter.getPIN(3)

		# Collimator off
		self.colli.off()

		# Output files
		# dtheta1,stagez,needle_y,collimator_y,z,
		#ofile.write("%8d %12.5f %12.5f %5.1f %5.1f"%(dt1_peak,stz_cen,ycenter,col_y,col_z))
		ofile.write("%8.5f %8d %12.5f %5.1f %5.1f %s\n"%(energy,dt1_peak,stz_cen,col_y,col_z,cnt_str))
		ofile.close()

		return 1

	def getDt1(self):
		return self.mono.getDt1()

	# usage: after shutter
	def simpleCountBack(self,ch1,ch2,inttime,ndata):
		if self.isInit==False:
			self.init()
		# shutter close
		print "Shutter close: estimation of background"
		self.finishScan()
		# average back ground
		ave1,ave2=self.simpleCount(ch1,ch2,inttime,ndata)

		# shutter open
		print "Shutter open: estimation of actual count"
		self.prepScan()
		ave3,ave4=self.simpleCount(ch1,ch2,inttime,ndata,ave1,ave2)

		print "Average ch1: %8d ch2: %8d\n"%(ave3,ave4)
		return ave3,ave4

	def simpleCount(self,ch1,ch2,inttime,ndata,back1=0,back2=0):
		if self.isInit==False:
			self.init()
        	counter=Count(self.s,ch1,ch2)
        	f=File("./")

        	prefix="%03d"%f.getNewIdx3()
        	ofilename="%s_count.scn"%prefix
        	of=open(ofilename,"w")

        	# initialization
        	starttime=time.time()
		strtime=datetime.datetime.now()
        	of.write("#### %s\n"%starttime)
        	of.write("#### %s\n"%strtime)
        	ttime=0
        	for i in arange(0,ndata,1):
                	currtime=time.time()
                	ttime=currtime-starttime
                	ch1,ch2=counter.getCount(inttime)
			ch1=ch1-back1
			ch2=ch2-back2
                	of.write("12345 %8.4f %12d %12d\n" %(ttime,ch1,ch2))
        	of.close()
	
        	# file open
        	ana=AnalyzePeak(ofilename)
        	x,y1,y2=ana.prepData3(1,2,3)

        	py1=ana.getPylabArray(y1)
        	py2=ana.getPylabArray(y2)

        	mean1=py1.mean()
        	mean2=py2.mean()
        	std1=py1.std()
        	std2=py2.std()

		of=open(ofilename,"a")

        	of.write("COUNTER1:%5d Average: %12.5f Std.:%12.5f (%8.3f perc.)\n"%(ch1,py1.mean(),py1.std(),py1.std()/py1.mean()*100.0))
        	of.write("COUNTER2:%5d Average: %12.5f Std.:%12.5f (%8.3f perc.)\n"%(ch2,py2.mean(),py2.std(),py2.std()/py2.mean()*100.0))

		of.close()
		return mean1,mean2

	def detuneID(self,energy,cnt1,cnt2,inttime,nback=30):
        	f=File("./")
		if self.isInit==False:
			self.init()
		# Set energy
		#self.changeE(energy)
		# Confirmation
		self.finishScan()
		print "Please set IC gain 1E5 or smaller and tune vias voltage."
		print "Push any keys when you finish..:"
		raw_input()
		# dtheta tune and detune 600pls
		#fwhm,center=self.dttune_id()
		
		# change gain 
		print "please set pin gain 1E10 and tune bias voltage."
		print "Push any keys when you finish..:"
		raw_input()

		# back ground estimation
		self.finishScan()
		ave1,ave2=self.simpleCount(cnt1,cnt2,inttime,nback)
		print "Back ground count : %8d %8d\n"%(ave1,ave2)

		# ID gap offset
		print "From now ID gap is detuned."
		self.prepScan()
        	prefix="%03d"%(f.getNewIdx3())
        	current_id=self.id.getE(energy)
		if energy<=12.4:
        		start=current_id
        		end=current_id+2
			step=0.1

		else:
        		start=current_id
        		end=current_id+5
			step=0.5

        	max1=self.id.scanID(prefix,start,end,step,cnt1,cnt2,inttime)
		print "ID detune finished."

		# Back ground subtraction
		ofname=prefix+"_id.scn"
		infile=open(ofname,"r")
		
		lines=infile.readlines()
		infile.close()
		of=open(ofname,"w")
	
		save=0
		bestgap=0.0
		for line in lines:
			cols=line.split()
			value1=int(cols[2])-ave1
			value2=int(cols[3])-ave2
			if value1>10000 and value1<15000:
				bestgap=float(cols[1])
				save=value1
			of.write("%5s%12s %10d %10d\n"%(cols[0],cols[1],value1,value2))

		print bestgap,save

		of.close()

	################################
	# Last modified 120607
	# for XYZ stage implemtented to the monitor 
	################################
	def prepCapture(self):
		if self.isInit==False:
			self.init()
		## Zoom in
		self.zoom.go(0)

		## Cryo go up
		self.cryo.off()

		## BM on
		self.bm.onPika()

		## BS on
		self.bs.on()

	###########################
	# Last modified 120607
	# for XYZ stage implemtented to the monitor 
	###########################
	def finishCapture(self):
		if self.isInit==False:
			self.init()
		## BM off
		self.bm.offXYZ()
		## BS off
		self.bs.off()

	def captureBM(self,prefix,isTune=True):
		if self.isInit==False:
			self.init()

		# Attenuator setting
		if isTune==True:
			# Tune gain
			gain=self.cap.tuneGain()

		print "##### GAIN %5d\n"%gain

		### averaging center x,y
		path=os.path.abspath("./")
		prefix="%s/%s"%(path,prefix)
		x,y=self.cap.aveCenter(prefix,5)

		return x,y

	def dttune_id(self):
		if self.isInit==False:	
			self.init()
		prefix="%03d"%self.f.getNewIdx3()

		###################
		# Delta theta1 tune
		###################
        	fwhm,center=self.mono.scanDt1PeakConfig(prefix,"DTSCAN_IDDETUNE",self.tcs)
		return fwhm,center

	def dttune(self,prefix):
		if self.isInit==False:	
			self.init()
			self.isInit=True
		# Delta theta1 tune
        	fwhm,center=self.mono.scanDt1PeakConfig(prefix,"DTSCAN_AUTOTUNE",self.tcs)

		return fwhm,center

	def dttuneMode(self,prefix,mode):
		if self.isInit==False:	
			self.init()
			self.isInit=True
		# Delta theta1 tune
        	fwhm,center=self.mono.scanDt1PeakConfig(prefix,mode,self.tcs)

		return fwhm,center

	def monI(self,outfile):
		of=open(outfile,"w")

		# Fixed point 
       		starttime=time.time()
		strtime=datetime.datetime.now()
       		of.write("#### %s\n"%strtime)
       		ttime=0
		counter=Count(self.s,self.fixed_ch1,self.fixed_ch2)

        	while (ttime <= self.block_time ):
                	currtime=time.time()
                	ttime=currtime-starttime
                	ch1,ch2=counter.getCount(self.count_time)
                	of.write("12345  %8.3f %12d %12d\n" %(ttime,ch1,ch2))
			of.flush()

		strtime=datetime.datetime.now()
        	of.write("#### %s\n"%strtime)
        	of.close()

	def readEtable(self,from_en,to_en):
		# reading table file
		fname="/isilon/BL32XU/BLtune/energy.tbl"
		tbf=open(fname,"r")
		lines=tbf.readlines()

		for line in lines:
			col1=line.split()[0]
			if col1=="#":
				continue
			tmpen=float(line.split()[0])
			if tmpen==energy:
				tbf.close()
				return line

		return "false"

	def moveEtable(self,energy):
		base_energy=12.3984
		# init
		if self.isInit==False:
			self.init()
		# table file reading
		base=self.readEtable(base_energy) # base energy table parameters
		toen=self.readEtable(energy)
		if base=="false" or toen=="false":
			sys.exit(1)
		print "base"+base
		print "to--"+toen

	def changeEandTune(self,energy,sleep_time=0):
		# sleep_time[sec]  	: wait time for tuning low energy
		# dt1_option	: delta theta 1 option
		# Example : DTSCAN_NORMAL, DTSCAN_LOWENERGY

        	if energy <8.5 or energy>20.0:
                	print "Invalid energy : 8.5 - 20.0 keV"
                	sys.exit(1)
	
        	if energy < 10.0:
                	option="DTSCAN_LOWENERGY"
        	else:
                	option="DTSCAN_NORMAL"

		# Move mono & ID gap
		self.changeE(energy)

		if self.isInit==False:
			self.init()

                prefix="%03d"%(self.f.getNewIdx3())
		time.sleep(sleep_time)
                dt1_fwhm,dt1_peak=self.mono.scanDt1PeakConfig(prefix,option,self.tcs)

		return dt1_fwhm,dt1_peak

	def changeE(self,energy):
		# energy[keV] 	: set to this energy 
		# Initialization check
		if self.isInit==False:
			self.init()

		# Energy change
    		self.mono.changeE(energy)

		# Gap
    		self.id.moveE(energy)

	def fixedPoint(self,energy,hours):
		# preparation
		if self.isInit==False:
			self.init()

		# dtheta1 tune
		prefix="%03d_dtheta1"%self.f.getNewIdx3()

		# change energy
		self.changeE(energy)
		self.dttune(prefix)

		# 2 hour BM
		logname="%03d_logf.dat"%(self.f.getNewIdx3())
		logf=open(logname,"w")

		mins=int(float(hours)*60.0)
		for i in range(0,mins):
			prefix="%03d_%04d"%(self.f.getNewIdx3(),i)
			x,y=self.captureBM(prefix)
			logf.write("XY= %8.3f %8.3f\n"%(x,y))
			time.sleep(60)

        def doSimpleMonitor(self,prefix):
                # initialize axes
                self.init()
		# BM off position
                self.bm.set(-60000)
		self.bs.set(0)
                # Reading config file
                self.readConfig()

		# Attenuator setting
		en=self.mono.getE()
		if en>11.0:
        		self.att.att1000um()
		else:
			self.att.att0um()

		# dtheta1 tune
		tmp="%s_dttune"%prefix
		self.dttune(tmp)

        	# current directory
        	curr_dir=self.f.getAbsolutePath()

		# StageAuto tune
        	st=StageTune(self.stage,self.cap,self.bm)

		# open ofile
		ofile=open("bm.dat","w")

                for iloop in range(0,self.total_num):
                        # BM off
                        self.bm.set(-60000)

                        # Capture beam position
                        path=os.path.abspath("./")
                        tmpname="%s/%03d_before.ppm"%(path,self.f.getNewIdx3())
                        ini_x,ini_y=self.captureBM(tmpname)

                        # Stage auto tune
        		filename="%s/%03d_st_before.ppm"%(curr_dir,self.f.getNewIdx3())
        		st.doAutomatic(filename)

                        # Fixed point
                        filename="%03d_fixed.scn"%(self.f.getNewIdx3())
                        self.monI(filename)

                        # Capture beam position
                        path=os.path.abspath("./")
                        tmpname="%s/%03d_after.ppm"%(path,self.f.getNewIdx3())
                        las_x,las_y=self.captureBM(tmpname)

			# writing log file
			ofile.write("%5d, %8.2f, %8.2f, %8.2f %8.2f\n"%(iloop,ini_x,ini_y,las_x,las_y))
		ofile.close()

        def monitorBP(self,prefix):
                # initialize axes
                self.init()

		# Preparation
		self.bs

		# BM off position
                self.bm.set(0)
		self.bs.goOn()
		self.shutter.open()
		
                # Reading config file
                self.readConfig()

		# Attenuator setting
		en=self.mono.getE()

		if en>11.0:
        		self.att.att1000um()
		else:
			self.att.att0um()

		# dtheta1 tune
		tmp="%s_dttune"%prefix
		self.dttune(tmp)

        	# current directory
        	curr_dir=self.f.getAbsolutePath()

		# open ofile
		ofile=open("bm.dat","w")

                # Tuning the gain of coax-camera
                gain=self.cap.tuneGain()

		y_total=0.0
		z_total=0.0
                for i in range(0,5):
                        # caputure and analyze
                        y,z=self.cap.aveCenter(prefix,gain)

                        # pixel to micron [um/pixel] in high zoom
                        p2u_z=7.1385E-2
                        p2u_y=9.770E-2

                        z_move=-dz*p2u_z
                        y_move=dy*p2u_y

			y_total+=y_move
			z_total+=z_total

		#### average position
		y_ave=y_total/5.0
		z_ave=z_total/5.0

                filename="%03d_fixed.scn"%(self.f.getNewIdx3())
                self.monI(filename)
		ofile.close()

if __name__=="__main__":
        host = '172.24.242.41'
        port = 10101
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host,port))

	proc=Procedure(s)
	print proc.captureBM("TEST")
	#en_list=arange(19.5,8.0,-0.5)
	#print en_list,len(en_list)

	#en_list=[19.5,15.5,12.5,11.5,11.0,10.5,10.4,10.3,10.2,10.1,10.0,9.9,9.8,9.7,9.6,9.5,8.5]
	#en_list=[19.5,15.5,12.3984,11.5,10.5,9.5,8.5]
	en_list=[8.5,9.5,10.5,11.5,12.3984,15.5,19.5]
	#en_list=arange(8.5,11.0,0.1)
	#print en_list
	#print len(en_list)

	#while(1):
		#for en in en_list:
			#proc.makeTable(en)

	# Analyze knife
	#print proc.analyzeKnife("049_stagey.scn")
	
	# Energy table check
	#proc.moveEtable(8.5)
