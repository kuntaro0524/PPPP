#!/bin/env python 
import sys
import socket
import time

# My library
from Received import *
from Motor import *
from MyException import *
from BSSconfig import *

#
class BS:
	def __init__(self,server):
		self.s=server
    		self.bs_y=Motor(self.s,"bl_32in_st2_bs_1_y","pulse")
    		self.bs_z=Motor(self.s,"bl_32in_st2_bs_1_z","pulse")
		
		self.isInit=False
		self.v2p=2000
		
		# Default value
		self.off_pos=-60000 # pulse
		self.on_pos=0 # pulse

	def getEvacuate(self):
		bssconf=BSSconfig()

        	try:
			tmpon,tmpoff=bssconf.getBS()
        	except MyException,ttt:
                	print ttt.args[0]

		self.on_pos=float(tmpon)*self.v2p
		self.off_pos=float(tmpoff)*self.v2p

		self.isInit=True
		print self.on_pos,self.off_pos

	def go(self,pvalue):
		self.bs_z.nageppa(pvalue)
	
	def on(self):
		if self.isInit==False:
			self.getEvacuate()
		self.bs_z.move(self.on_pos)

	def off(self):
		if self.isInit==False:
			self.getEvacuate()
		self.bs_z.move(self.off_pos)

	def goOn(self):
		if self.isInit==False:
			self.getEvacuate()
		self.go(self.on_pos)

	def goOff(self):
		if self.isInit==False:
			self.getEvacuate()
		self.go(self.off_pos)

if __name__=="__main__":
	host = '172.24.242.41'
	port = 10101
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host,port))

	print "Moving BS"
	print "type on/off:"
	#option=raw_input()
	bs=BS(s)
	bs.go(-30000)

	#bs.getEvacuate()

	#if option=="on":
		#bs.on()
	#elif option=="off":
		#bs.off()
	s.close()
