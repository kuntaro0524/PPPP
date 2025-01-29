#!/bin/env python 
import sys
import socket
import time

# My library
from Received import *
from Motor import *
from AnalyzePeak import *
from File import *
from AxesInfo import *
from ConfigFile import *
from Count import *

class ExSlit2:

	def __init__(self,server):
		self.s=server
    		self.blade_upper=Motor(self.s,"bl_32in_st2_slit_2_upper","pulse")
    		self.blade_lower=Motor(self.s,"bl_32in_st2_slit_2_lower","pulse")
    		self.blade_hall=Motor(self.s,"bl_32in_st2_slit_2_hall","pulse")
    		self.blade_ring=Motor(self.s,"bl_32in_st2_slit_2_ring","pulse")

	def fullOpen(self):
		self.setSize(1000,1000)

	def setUpper(self,position):
		self.blade_upper.move(-position)

	def setLower(self,position):
		self.blade_lower.move(-position)

	def setRing(self,position):
		self.blade_ring.move(-position)

	def setHall(self,position):
		self.blade_hall.move(-position)

	def setSize(self,v_apert,h_apert):
		# Back lash
		#self.setUpper(1000)
		#self.setLower(-1000)
		#self.setRing(-1000)
		#self.setHall(1000)
		
		# v_apert and h_apert should be 'even' number
		vert_move=int(v_apert/2.0)
		hori_move=int(h_apert/2.0)
		
		self.setUpper(vert_move)
		self.setLower(-vert_move)
		self.setHall(hori_move)
		self.setRing(-hori_move)
		
        def scanV(self,prefix,start,end,step,cnt_ch1,cnt_ch2,time):
                # Scan setting
                self.blade_upper.setStart(-1*start)
                self.blade_upper.setEnd(-1*end)
                self.blade_upper.setStep(-1*step)

		# output file
		ofile="%s_slit2_vert.scn"%prefix
		self.blade_upper.axisScan(ofile,cnt_ch1,cnt_ch2,time)

                # Analysis and Plot
		comment=AxesInfo(self.s).getLeastInfo()
                ana=AnalyzePeak(ofile)
                fwhm,center=ana.anaK("slit2 upper[pulse]","intensity[cnt]",comment)
		return fwhm,center

        def scanH(self,prefix,start,end,step,cnt_ch1,cnt_ch2,time):
                # Scan setting
                self.blade_ring.setStart(-1*start)
                self.blade_ring.setEnd(-1*end)
                self.blade_ring.setStep(-1*step)

		# output file
		ofile="%s_slit2_hori.scn"%prefix
		self.blade_ring.axisScan(ofile,cnt_ch1,cnt_ch2,time)

                # Analysis and Plot
		comment=AxesInfo(self.s).getLeastInfo()

                ana=AnalyzePeak(ofile)
                fwhm,center=ana.anaK("slit2 ring[pulse]","intensity[cnt]",comment)
		return fwhm,center

if __name__=="__main__":
	host = '172.24.242.41'
	port = 10101
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host,port))

	print "prog PREFIX CHANNEL"
	test=ExSlit2(s)
	count=Count(s,3,0)

	# Flags for scan
	f_horiscan=True
	f_vertscan=False

	# Horizontal aperture test
	if f_horiscan:
		test.fullOpen()
		logf=open("hori.dat","w")
		for hapert in arange(500,0,-20):
			test.setSize(1000, hapert)
			cntstr=count.getPIN(3)
			logf.write("%5d %s\n"%(hapert,cntstr))
		test.setSize(5000,5000)
		logf.close()

	# Vertical aperture test
	if f_vertscan:
		logf=open("vert.dat","w")
		test.fullOpen()
		for vapert in arange(120,0,-4):
			test.setSize(vapert, 1000)
			cntstr=count.getPIN(3)
			logf.write("%5d %s\n"%(vapert,cntstr))
		logf.close()

	test.fullOpen()
	s.close()
