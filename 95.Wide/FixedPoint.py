#!/bin/env python
import sys
import socket
import time
import datetime

# My library
from File import *
from ExSlit2 import *
from BM import *
from Capture import *
from Count import *
from Mono import *
from ConfigFile import *
from Att import *
from BeamCenter import *
from Stage import *
from StageTune import *

class FixedPoint:
	def __init__(self,server):
		self.s=server

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
		self.bm=BM(self.s)
       		self.f=File("./")
		self.cap=Capture()
		self.slit2=ExSlit2(self.s)
        	self.att=Att(self.s)
        	self.stage=Stage(self.s)

	def captureBM(self,filename):
		# Attenuator setting
		en=self.mono.getE()
		print "en %8.3f\n"%en
		if en>11.0:
        		self.att.att1000um()
		else:
			self.att.att0um()

		# BM preparation
		self.bm.set(0)

		# Capture before fixed point scan
       		self.cap.capture(filename)
		self.bm.set(-60000)

		# Acquire beam center position from PPM file
		try :
			bc=BeamCenter(filename)
			x,y=bc.find()

        	except MyException,ttt:
                	print ttt.args[0]
                	print "Check your config file carefully.\n"
			# Attenuator setting
			#self.att.att0um()
			return 0,0

		# Attenuator setting
		#self.att.att0um()
		
		return x,y

	def dttuneRecover(self,prefix):
		# Slit2 narrow setting FWHM at Slit2@12.398
		self.slit2.setSize(35,250)
	
		# Delta theta1 tune
        	fwhm,center=self.mono.scanDt1Peak(prefix,self.scan_dt1_start,self.scan_dt1_end,self.scan_dt1_step,self.scan_dt1_ch1,self.scan_dt1_ch2,self.scan_dt1_time)

		# Slit2 open aperture 
		self.slit2.setSize(2000,2000)
		
		return fwhm,center

	def dttune(self,prefix):
		# Delta theta1 tune
        	fwhm,center=self.mono.scanDt1Peak(prefix,self.scan_dt1_start,self.scan_dt1_end,self.scan_dt1_step,self.scan_dt1_ch1,self.scan_dt1_ch2,self.scan_dt1_time)

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

	def doLongScan(self):
		# Reading config file
		self.readConfig()

		for iloop in range(0,self.total_num):
			# Fixed point
			filename="%s_fixed.scn"%(prefix)
			self.monI(filename)

	def doMonitor(self,prefix):
		# Reading config file
		self.readConfig()
		# initialize axes
		self.init()

		for iloop in range(0,self.total_num):
			# BM off
			self.bm.set(-60000)
		
			# Dtheta recover
			tmprefix="%s_init"%prefix
			ini_fwhm,ini_peak=self.dttuneRecover(tmprefix)

			# Capture beam position
			path=os.path.abspath("./")
			tmpname="%s/%s_before.ppm"%(path,prefix)
			ini_x,ini_y=self.captureBM(tmpname)

			# Fixed point
			filename="%s_fixed.scn"%(prefix)
			self.monI(filename)

			# Capture after fixed point scan
			tmpname="%s/%s_after.ppm"%(path,prefix)
			aft_x,aft_y=self.captureBM(tmpname)

			# Recover dtheta1
			tmprefix="%s_final"%prefix
			fin_fwhm,fin_peak=self.dttuneRecover(tmprefix)

			# Capture after recovering
			tmpname="%s/%s_final.ppm"%(path,prefix)
			fin_x,fin_y=self.captureBM(tmpname)

			# return value
			tmpstr1="dt1(ini,fin) =(%8d, %8d)"%(ini_peak,fin_peak)
			tmpstr2=" MonX(ini,fin)=(%8.3f, %8.3f)"%(ini_x,aft_x)
			tmpstr3=" MonY(ini,fin)=(%8.3f, %8.3f)"%(ini_y,aft_y)

			rtnstr=tmpstr1+tmpstr2+tmpstr3
	
			return rtnstr

        def doSimpleMonitor(self,prefix):
                # initialize axes
                self.init()
		# BM off position
                self.bm.set(-60000)
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

if __name__=="__main__":
        host = '172.24.242.41'
        port = 10101
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host,port))

	test=FixedPoint(s)
	prefix="PREFIX"
	test.doMonitor(prefix)
