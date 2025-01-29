#!/bin/env python 
import sys
import socket
import time

# My library
from Received import *
from Motor import *
from BSSconfig import *

#
class Colli:
	def __init__(self,server):
		self.s=server
    		self.coly=Motor(self.s,"bl_32in_st2_collimator_1_y","pulse")
    		self.colz=Motor(self.s,"bl_32in_st2_collimator_1_z","pulse")
		
		self.off_pos=-60000 # pulse
		self.on_pos=0 # pulse
		
		self.y_v2p=500 # pulse/mm
		self.z_v2p=2000 # pulse/mm

		self.isInit=False

	def go(self,pvalue):
		self.colz.nageppa(pvalue)

        def getEvacuate(self):
                bssconf=BSSconfig()

                try:
                        tmpon,tmpoff=bssconf.getColli()
                except MyException,ttt:
                        print ttt.args[0]

                self.on_pos=float(tmpon)*self.z_v2p
                self.off_pos=float(tmpoff)*self.z_v2p

                self.isInit=True
                print self.on_pos,self.off_pos
	
	def on(self):
		if self.isInit==False:
			self.getEvacuate()
		self.colz.move(self.on_pos)

	def off(self):
		if self.isInit==False:
			self.getEvacuate()
		self.colz.move(self.off_pos)

	def goOn(self):
		if self.isInit==False:
			self.getEvacuate()
		self.go(self.on_pos)

	def goOff(self):
		if self.isInit==False:
			self.getEvacuate()
		self.go(self.off_pos)

	def scanY(self,prefix,ch):
		print "ScanY"

	def scan(self,prefix,ch):
		ofile="%s_colliz.scn"%prefix

		self.current_z=self.colz.getPosition()
		print "Current value=%8d\n"%self.current_z

		scan_start=-500
		scan_end=500
		scan_step=20
		cnt_ch=ch
		cnt_ch2=1
		cnt_time=0
		unit="pulse"

        	self.colz.axisScan(self,ofile,scan_start,scan_end,scan_step,cnt_ch,cnt_ch2,cnt_time,unit)

if __name__=="__main__":
	host = '172.24.242.41'
	port = 10101

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host,port))

	coli=Colli(s)
	#coli.getEvacuate()
	coli.off()

	s.close()
