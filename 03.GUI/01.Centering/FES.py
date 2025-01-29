#!/bin/env python 
import sys
import socket
import time

# My library
from Received import *
from Organizer import *

# till 100404
#ini_width=0.298
#ini_height=0.267

# 100404-
ini_height=0.3095
ini_width=0.3120

class FES:

    def __init__(self,server):
	self.s=server
    	self.fe_height=Organizer(self.s,"bl_32in","fe_slit_1","height")
    	self.fe_width=Organizer(self.s,"bl_32in","fe_slit_1","width")
    	self.fe_vert=Organizer(self.s,"bl_32in","fe_slit_1","vertical")
    	self.fe_hori=Organizer(self.s,"bl_32in","fe_slit_1","horizontal")
	#print "FE"

    def moveInit(self):
	print "moving FES for (H,W)=(%8.4f,%8.4f)"%(ini_height,ini_width)
	self.fe_height.move(ini_height,"mm")
	self.fe_width.move(ini_width,"mm")
	
    def scan(self,prefix,cnt_ch1,cnt_ch2):
	# FE slit size -> (H,W)=(0.1,0.3)
	# 50um
	tmpheight=ini_height - 0.25
    	self.fe_height.move(tmpheight,"mm")

	# Setting
    	ofile=prefix+"_fes_vert.scn"
    	scan_start=-0.5
    	scan_end=1.5
    	scan_step=0.05
    	cnt_ch=1 # channel
    	cnt_time=0.2
    	unit="mm"
	
    	self.fe_vert.axisScan(ofile,scan_start,scan_end,scan_step,cnt_ch1,cnt_ch2,cnt_time,unit)
	
	# FE slit size -> (H,W)=(0.3,0.1)
    	self.fe_height.move(ini_height,"mm")
	tmpwidth=ini_width - 0.25
    	self.fe_width.move(tmpwidth,"mm")
	
	# Setting
    	ofile=prefix+"_fes_hori.scn"
    	scan_start=-1.8
    	scan_end=1.8
    	scan_step=0.05
    	cnt_ch=1 # channel
    	cnt_time=0.2
    	unit="mm"
	
    	self.fe_hori.axisScan(ofile,scan_start,scan_end,scan_step,cnt_ch1,cnt_ch2,cnt_time,unit)
	# FE slit size -> (H,W)=(0.3,0.1)
    	self.fe_width.move(ini_width,"mm")
