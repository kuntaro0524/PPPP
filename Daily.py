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

class Daily:
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
		# Added on 2014/05/28 K.Hirata
		self.cover=Cover(self.s)
		self.clen=CCDlen(self.s)

#####################
#### CCD cover ######
#####################
	def coverOn(self):
		self.cover.on()
		if self.cover.isCover():
			print "CCD cover ON finished"

	def coverOff(self):
		self.cover.on()
		print "CCD cover ON"

#####################
#### Shutter   ######
#####################
	def openShutter(self):
        	self.slit1.openV()
        	self.light.off()
        	self.shutter.open()

	def closeShutter(self):
        	self.shutter.close()
        	self.slit1.closeV()

	def finishScan(self):
		self.slit1.closeV()
		self.shutter.close()

####################
#### Monochromator #
####################
	def dttune(self,prefix):
		if self.isInit==False:	
			self.init()
			self.isInit=True
		# Delta theta1 tune
        	fwhm,center=self.mono.scanDt1PeakConfig(prefix,"DTSCAN_NORMAL",self.tcs)
		return fwhm,center

	def changeE(self,energy):
		# energy[keV] 	: set to this energy 
		# Initialization check
		if self.isInit==False:
			self.init()

		# Energy change
    		self.mono.changeE(energy)

		# Gap
    		self.id.moveE(energy)

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
