#!/bin/env python 
import sys
import socket
import time

# My library
from Received import *
from Organizer import *
from AnalyzeData import *


class DthetaTune:
 
    def __init__(self,srv):
	self.srv=srv
    	self.stmono=Organizer(srv,"bl_32in","tc1_stmono_1","dtheta1")
	self.scan_step=0
	self.scan_start=0
	self.scan_end=0

    def do(self,prefix,cnt_ch1,cnt_ch2):
	# Setting
        ofile=prefix+"_dtheta1.scn"
    	self.scan_start=-89000
    	self.scan_end=-85000

	if self.scan_step==0:
    		self.scan_step=100

    	cnt_time=0.2
    	unit="pulse"

    	maxval=self.stmono.axisScan(ofile,self.scan_start,self.scan_end,self.scan_step,cnt_ch1,cnt_ch2,cnt_time,unit)
	ana=AnalyzeData(ofile,"peak")
	ppp=ana.analyze(1,2)  # the first counter

	print "FWHM: %12.5f %12.5f"%(ppp[0],ppp[1])
	self.stmono.move(int(ppp[1]),"pulse")
	print "Final position: %s%s" % (ppp[1],"pulse")

	return int(ppp[1])
  

    def setStep(self,step):
	self.scan_step=step

    def setStart(self,start):
	self.scan_start=start

    def setEnd(self,end):
	self.scan_end=end

    def doFine(self,prefix,cnt_ch1,cnt_ch2):
	# Setting
        ofile=prefix+"_dtheta1.scn"

	if self.scan_start==0:
    		self.scan_start=-88000
	if self.scan_end==0:
    		self.scan_end=-85000
	if self.scan_step==0:
    		self.scan_step=20

    	cnt_time=0.2
    	unit="pulse"

    	maxval=self.stmono.axisScan(ofile,self.scan_start,self.scan_end,self.scan_step,cnt_ch1,cnt_ch2,cnt_time,unit)
	ana=AnalyzeData(ofile,"peak")
	ppp=ana.drvCenter(1,2)  #

	print "Center: %12.5f"%(ppp)
	self.stmono.move(int(ppp),"pulse")
	print "Final position: %s%s" % (ppp,"pulse")

    def scanStep(self,prefix,cnt_ch1,cnt_ch2,step):
	# Setting
        ofile=prefix+"_dtheta1.scn"
	if self.scan_start==0:
    		self.scan_start=-88000
	if self.scan_end==0:
    		self.scan_end=-85000
	if self.scan_step==0:
    		self.scan_step=20

    	cnt_time=0.2
    	unit="pulse"

    	maxval=self.stmono.axisScan(ofile,self.scan_start,self.scan_end,self.scan_step,cnt_ch1,cnt_ch2,cnt_time,unit)
	ana=AnalyzeData(ofile,"peak")
	ppp=ana.drvCenter(1,2)  #

	print "Center: %12.5f"%(ppp)
	self.stmono.move(int(ppp),"pulse")
	print "Final position: %s%s" % (ppp,"pulse")

if __name__=="__main__":
	host = '172.24.242.41'
	port = 10101
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host,port))
	
	dtheta=DthetaTune(s)
	dtheta.do(sys.argv[1],1,2)

	s.close()
