#!/bin/env python 
import sys
import socket
import time

# My library
from Received import *
from Organizer import *


class ExSlit1:

	def __init__(self,server,cnt_ch):
		self.s=server
		self.cnt_ch=cnt_ch
    		self.blade_upper=Organizer(self.s,"bl_32in","st2_slit_1","upper")
    		self.blade_ring=Organizer(self.s,"bl_32in","st2_slit_1","ring")

	def fullOpen(self):
		self.blade_upper.move(10000,"pulse")
		self.blade_ring.move(-10000,"pulse")

	def scanVertical(self,outfilename):
		# Setting
    		scan_start=3710
    		scan_end=10
    		scan_step=-50
    		cnt_time=0.2
		unit="pulse"
    		self.blade_upper.axisScan(outfilename,scan_start,scan_end,scan_step,self.cnt_ch,self.cnt_ch+1,cnt_time,unit)

	def scanVerticalBack(self,outfilename):
		# Setting
    		scan_start=10
    		scan_end=3710
    		scan_step=50
    		cnt_time=0.2
		unit="pulse"
    		self.blade_upper.axisScan(outfilename,scan_start,scan_end,scan_step,self.cnt_ch,self.cnt_ch+1,cnt_time,unit)

	def scanHorizontal(self,outfilename):
		# Setting
    		scan_start=-8000
    		scan_end=-3000
    		scan_step=50
    		cnt_time=0.2
    		unit="pulse"
    		self.blade_ring.axisScan(outfilename,scan_start,scan_end,scan_step,self.cnt_ch,self.cnt_ch+1,cnt_time,unit)

	def scanHorizontalBack(self,outfilename):
		# Setting
    		scan_start=3000
    		scan_end=-8000
    		scan_step=-50
    		cnt_time=0.2
    		unit="pulse"
    		self.blade_ring.axisScan(outfilename,scan_start,scan_end,scan_step,self.cnt_ch,self.cnt_ch+1,cnt_time,unit)

	def scanBoth(self,prefix):
		vf="%s_sts1_vert.scn"%prefix
		hf="%s_sts1_hori.scn"%prefix

		self.scanVertical(vf)
		self.scanHorizontal(hf)


if __name__=="__main__":
	host = '172.24.242.41'
	port = 10101
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host,port))

	print "prog PREFIX CHANNEL"
	test=ExSlit1(s,int(sys.argv[2]))
	test.fullOpen()
	test.scanBoth(sys.argv[1])
