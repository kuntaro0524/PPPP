#!/bin/env python 
import sys
import socket
import time

# My library
from Received import *
from Organizer import *
from AnalyzeData import *


class TCS:

	def __init__(self,server):
		self.s=server
    		self.tcs_height=Organizer(self.s,"bl_32in","tc1_slit_1","height")
    		self.tcs_width=Organizer(self.s,"bl_32in","tc1_slit_1","width")
    		self.tcs_vert=Organizer(self.s,"bl_32in","tc1_slit_1","vertical")
    		self.tcs_hori=Organizer(self.s,"bl_32in","tc1_slit_1","horizontal")

	def getApert(self):
		# get values
		self.ini_height=self.tcs_height.getAperture()
		self.ini_width=self.tcs_width.getAperture()
		print self.ini_height,self.ini_width

	def setPosition(self,vert,hori,unit):
		# get values
    		self.tcs_vert.move(vert,unit)
    		self.tcs_hori.move(hori,unit)

	def setApert(self,height,width):
		# get values
		self.height=float(height)
		self.width=float(width)

		# check values
		if self.height<0.02 or self.width < 0.02 :
			print "TCS abort!!! check width or height"
			sys.exit()
		elif self.height>10.0 or self.width > 10.0:
			print "TCS abort!!! check width or height"
			sys.exit()

		# set
		self.tcs_height.move(self.height,"mm")
		self.tcs_width.move(self.width,"mm")
		print "current tcs aperture : %8.5f %8.5f\n" %(self.height,self.width)

	def scan(self,prefix,cnt_ch1,cnt_ch2):
		# Horizontal scan setting
    		ofile=prefix+"_tcs_vert.scn"
    		scan_start=-1.0   # use in Fixed-exit with slit before mirror
    		scan_end=1.0      # use in Fixed-exit with slit before mirror
    		scan_step=0.05
    		cnt_time=0.5
    		unit="mm"

		self.setApert(0.05,0.20)
    		self.tcs_vert.axisScan(ofile,scan_start,scan_end,scan_step,cnt_ch1,cnt_ch2,cnt_time,unit)

        	ana=AnalyzeData(ofile,"peak")
        	self.vertdata=ana.analyze(1,2)  # the first counter

        	print "FWHM: %12.5f %12.5f"%(self.vertdata[0],self.vertdata[1])
        	self.tcs_vert.move(self.vertdata[1],unit)
        	print "Final position: %s%s" % (self.vertdata[1],unit)

		# Setting
    		ofile=prefix+"_tcs_hori.scn"
    		scan_start=-1.0
    		scan_end=1.0
    		scan_step=0.05
    		cnt_time=0.5
    		unit="mm"
		
		self.setApert(0.20,0.05)
    		self.tcs_hori.axisScan(ofile,scan_start,scan_end,scan_step,cnt_ch1,cnt_ch2,cnt_time,unit)
		
        	ana=AnalyzeData(ofile,"peak")
        	self.horidata=ana.analyze(1,2)  # the first counter

        	print "FWHM: %12.5f %12.5f"%(self.horidata[0],self.horidata[1])
        	self.tcs_hori.move(float(self.horidata[1]),unit)
        	print "Final position: %s%s" % (self.horidata[1],unit)

	def scanV(self,prefix,cnt_ch1,start,end,step,time,unit):
		# Horizontal scan setting
    		ofile=prefix+"_tcs_vert.scn"

		self.setApert(0.05,1.00)
    		self.tcs_vert.axisScan(ofile,start,end,step,cnt_ch1,cnt_time,unit)

        	ana=AnalyzeData(ofile,"peak")
        	ppp=ana.drvCenter(1,2)  # the first counter

        	print "FWHM center: %12.5f"%(ppp)
        	self.tcs_vert.move(ppp,unit)
        	print "Final position: %s%s" % (ppp,unit)

		ofile.close()

	def scanH(self,prefix,cnt_ch1,start,end,step,time,unit):
		# Setting
    		ofile=prefix+"_tcs_hori.scn"

		self.setApert(1.00,0.05)
    		self.tcs_hori.axisScan(ofile,start,end,step,cnt_ch1,cnt_time,unit)
		
        	ana=AnalyzeData(ofile,"peak")
        	ppp=ana.drvCenter(1,2)  # the first counter

        	print "FWHM center: %12.5f"% ppp
        	self.tcs_hori.move(ppp,unit)
        	print "Final position: %s%s" % (ppp,unit)

	def scanVerbose(self,prefix,cnt_ch1,cnt_ch2):
		# Horizontal scan setting
    		ofile=prefix+"_tcs_vert.scn"
    		#scan_start=-2.0   # use in Fixed-exit with Ty1 axis
    		#scan_end=2.0      # use in Fixed-exit with Ty1 axis
    		scan_start=-1.0   # use in Fixed-exit with slit before mirror
    		scan_end=1.0      # use in Fixed-exit with slit before mirror
    		scan_step=0.05
    		cnt_time=0.5
    		unit="mm"

		self.setApert(0.05,1.00)
    		self.tcs_vert.axisScan(ofile,scan_start,scan_end,scan_step,cnt_ch1,cnt_ch2,cnt_time,unit)

        	ana=AnalyzeData(ofile,"peak")
        	ppp=ana.analyze(1,2)  # the first counter

        	print "FWHM: %12.5f center %12.5f"%(ppp[0],ppp[1])
		print "Input TCS vertical:"
		finalvalue=float(raw_input())
        	self.tcs_vert.move(finalvalue,unit)

		# Setting
    		ofile=prefix+"_tcs_hori.scn"
    		scan_start=-2.0
    		scan_end=2.0
    		scan_step=0.05
    		cnt_time=0.5
    		unit="mm"
		
		self.setApert(1.00,0.05)
    		self.tcs_hori.axisScan(ofile,scan_start,scan_end,scan_step,cnt_ch1,cnt_ch2,cnt_time,unit)
		
        	ana=AnalyzeData(ofile,"peak")
        	ppp=ana.analyze(1,2)  # the first counter

        	print "FWHM: %12.5f center %12.5f"%(ppp[0],ppp[1])
		print "Input TCS vertical:"
		finalvalue=float(raw_input())
        	self.tcs_hori.move(finalvalue,unit)

	def scanFixedApert(self,prefix,cnt_ch1,cnt_ch2):
		# Horizontal scan setting
    		ofile=prefix+"_tcs_vert.scn"
    		scan_start=start
    		scan_end=end
    		scan_step=0.05
    		cnt_time=0.5
    		unit="mm"

    		self.tcs_vert.axisScan(ofile,scan_start,scan_end,scan_step,cnt_ch1,cnt_ch2,cnt_time,unit)
        	ana=AnalyzeData(ofile,"peak")
        	ppp=ana.analyze(1,2)  # the first counter

        	print "FWHM: %12.5f %12.5f"%(ppp[0],ppp[1])
        	self.tcs_vert.move(ppp[1],unit)
        	print "Final position: %s%s" % (ppp[1],unit)

		# Setting
    		ofile=prefix+"_tcs_hori.scn"
    		scan_start=-2.0
    		scan_end=2.0
    		scan_step=0.05
    		cnt_time=0.5
    		unit="mm"
		
    		self.tcs_hori.axisScan(ofile,scan_start,scan_end,scan_step,cnt_ch1,cnt_ch2,cnt_time,unit)
		
        	ana=AnalyzeData(ofile,"peak")
        	ppp=ana.analyze(1,2)  # the first counter

        	print "FWHM: %12.5f %12.5f"%(ppp[0],ppp[1])
        	self.tcs_hori.move(float(ppp[1]),unit)
        	print "Final position: %s%s" % (ppp[1],unit)


	def checkZeroV(self,prefix,start,end,step,time,cnt_ch1):

		self.setApert(1.00,1.00)

		ofile=prefix+"_vert_zero.scn"
    		scan_start=start
    		scan_end=end
    		scan_step=step
    		cnt_time=time
    		unit="mm"

		ndata=int((scan_end-scan_start)/scan_step)+1
		if ndata <=0 :
			print "Set correct scan step!!\n"
			return 1

		if scan_end<0.015:
			print "Set larger slit size!!\n"
			return 1

		outfile=open(ofile,"w")

		for x in range(0,ndata):
			value=scan_start+x*scan_step
			self.setApert(value,0.1)
			count=self.tcs_vert.getCount(cnt_ch1,cnt_time)
			outfile.write("%12.5f %12.5f\n"%(value,count))

		self.setApert(1.0,1.0)
		return 1

	def checkZeroH(self,prefix,start,end,step,time,cnt_ch1):

		self.setApert(1.0,1.0)

		ofile=prefix+"_hori_zero.scn"
    		scan_start=start
    		scan_end=end
    		scan_step=step
    		cnt_time=time
    		unit="mm"

		ndata=int((scan_end-scan_start)/scan_step)+1
		if ndata <=0 :
			print "Something wrong"
			return 1

		if scan_end<0.015:
			print "Set larger slit size!!\n"
			return 1

		outfile=open(ofile,"w")

		for x in range(0,ndata):
			value=scan_start+x*scan_step
			self.setApert(0.1,value)
			count=self.tcs_hori.getCount(cnt_ch1,cnt_time)
			outfile.write("%12.5f %12.5f\n"%(value,count))

		self.setApert(1.0,1.0)
		return 1

if __name__=="__main__":
        host = '172.24.242.41'
        port = 10101
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host,port))

        tcs=TCS(s)

	prefix=raw_input()
        tcs.checkZeroH("TEST",1.0,0.1,-0.1,0.2,2)
	#def checkZeroH(self,prefix,start,end,step,time,cnt_ch1):

        s.close()
