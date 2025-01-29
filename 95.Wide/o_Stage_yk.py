#!/bin/env python 
import sys
import socket
import time

# My library
from Received import *
from Motor import *
from AnalyzePeak import *
from AxesInfo import *

class STAGE:

	def __init__(self,server):
		self.s=server
    		self.stage_z=Motor(self.s,"bl_32in_st2_stage_1_z","pulse")
    		self.stage_y=Motor(self.s,"bl_32in_st2_stage_1_y","pulse")

		# each blade
    		self.exslit2_ring= Motor(self.s,"bl_32in_st2_slit_2_ring","pulse")
    		self.exslit2_hall= Motor(self.s,"bl_32in_st2_slit_2_hall","pulse")
    		self.exslit2_upper=Motor(self.s,"bl_32in_st2_slit_2_upper","pulse")
    		self.exslit2_lower=Motor(self.s,"bl_32in_st2_slit_2_lower","pulse")

	def getPosition(self):
		# get values
    		self.tcs_vert.move(vert)
    		self.tcs_hori.move(hori)

	def setPosition(self,vert,hori):
		# get values
    		self.tcs_vert.move(vert)
    		self.tcs_hori.move(hori)

	def setApert(self,upper,ring):
		self.exslit2_upper.move(upper)
		self.exslit2_ring.move(ring)
		print "current ExSlit2 Position (Upper, Ring): %8.5f %8.5f\n" %(upper,ring)

	def scanBoth(self,prefix,scan_width,another_width,start,end,step,cnt_ch1,cnt_ch2,time):
		vfwhm,vcenter=self.scanV(prefix,scan_width,another_width,start,end,step,cnt_ch1,cnt_ch2,time)
		hfhwm,hcenter=self.scanH(prefix,another_width,scan_width,start,end,step,cnt_ch1,cnt_ch2,time)

		return vcenter,hcenter

	def scanV(self,prefix,height,width,start,end,step,cnt_ch1,cnt_ch2,time):
		# Vertical scan setting
    		ofile=prefix+"_tcs_vert.scn"
	
		# Aperture setting
		self.setApert(height,width)

		# Scan setting 
		self.tcs_vert.setStart(start)
		self.tcs_vert.setEnd(end)
		self.tcs_vert.setStep(step)

    		self.tcs_vert.axisScan(ofile,cnt_ch1,cnt_ch2,time)

		# AnalyzePeak
                ana=AnalyzePeak(ofile)
                outfig=prefix+"_tcs_vert.png"

                comment=AxesInfo(self.s).getLeastInfo()
                fwhm,center=ana.analyzeAll("TCS vert[mm]","Intensity",outfig,comment,"OBS")

                self.tcs_vert.move(center)
                print "Final position: %smm" % (center)
		return fwhm,center

	def scanH(self,prefix,height,width,start,end,step,cnt_ch1,cnt_ch2,time):
		# Horizontal scan setting
    		ofile=prefix+"_tcs_hori.scn"

		# Aperture setting
		self.setApert(height,width)

		# Scan setting 
		self.tcs_hori.setStart(start)
		self.tcs_hori.setEnd(end)
		self.tcs_hori.setStep(step)
		
    		self.tcs_hori.axisScan(ofile,cnt_ch1,cnt_ch2,time)

		# AnalyzePeak
                ana=AnalyzePeak(ofile)
                outfig=prefix+"_tcs_hori.png"

                comment=AxesInfo(self.s).getLeastInfo()
                fwhm,center=ana.analyzeAll("TCS hori[mm]","Intensity",outfig,comment,"OBS")

                self.tcs_hori.move(center)
		return fwhm,center

	def checkZeroV(self,prefix,start,end,step,cnt_ch1,cnt_ch2,time):
                # Counter
                counter=Count(self.s,cnt_ch1,cnt_ch2)

		# Setting aperture
		self.setApert(1.00,1.00)

		ofile=prefix+"_vert_zero.scn"

    		scan_start=start
    		scan_end=end
    		scan_step=step
    		cnt_time=time

		ndata=int((scan_end-scan_start)/scan_step)+1
		if ndata <=0 :
			print "Set correct scan step!!\n"
			return 1

		outfile=open(ofile,"w")

		for x in range(0,ndata):
			value=scan_start+x*scan_step
			self.setApert(value,1.0)
                        count1,count2=counter.getCount(cnt_time)
                        count1=float(count1)
                        count2=float(count2)
                        outfile.write("%12.5f %12.5f %12.5f\n"%(value,count1,count2))

		self.setApert(1.0,1.0)
		return 1

	def checkZeroH(self,prefix,start,end,step,cnt_ch1,cnt_ch2,time):
                # Counter
                counter=Count(self.s,cnt_ch1,cnt_ch2)

		# Setting aperture
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

		outfile=open(ofile,"w")

		for x in range(0,ndata):
			value=scan_start+x*scan_step
			self.setApert(1.0,value)
                        count1,count2=counter.getCount(cnt_time)
                        count1=float(count1)
                        count2=float(count2)
                        outfile.write("%12.5f %12.5f %12.5f\n"%(value,count1,count2))

		self.setApert(1.0,1.0)
		return 1

if __name__=="__main__":
        host = '172.24.242.41'
        port = 10101
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host,port))

        tcs=TCS(s)

	#tcs.checkZeroV("TEST",1.0,0.5,-0.1,0.2,1)

	#tcs.getApert()
	#tcs.setApert(0.1,0.1)
	#tcs.setPosition(1.000,-1.000)

	tcs.scanBoth("VVVV",0.05,0.50,-1.0,1.0,0.05,0,1,0.2)

	#tcs.setPosition(0.00052,0.00302)
	#prefix=raw_input()
        #tcs.checkZeroH("TEST",1.0,0.1,-0.1,1,2,0.2)
        #tcs.checkZeroV("TEST",1.0,0.1,-0.1,1,2,0.2)
	#def checkZeroH(self,prefix,start,end,step,time,cnt_ch1):

        s.close()
