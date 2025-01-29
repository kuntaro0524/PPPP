#!/bin/env python 
import sys
import socket
import time
import os

# My library
from Motor import *

class MirrorTuneUnit:
	def __init__(self,server):
		self.s=server
	# Motorized axes	
    		self.stage_y=Motor(self.s,"bl_32in_st2_motor_1","pulse")
    		self.stage_z=Motor(self.s,"bl_32in_st2_motor_2","pulse")

	# Initial settings
    		self.pin_to_bm_y=28750
    		self.pin_to_bm_z=10000
		self.y=0
		self.z=0

	def setPulse(self,option):
		# set up parameters
    		if option=="dire_pin":
			self.y=0
			self.z=0
			return 1

    		elif option=="hfm_pin":
			self.y=6300
			self.z=0
			return 1
		
    		elif option=="vfm_pin":
			self.y=0
			self.z=79800
			return 1

    		elif option=="both_pin":
			self.y=6300
			self.z=79800
			return 1

    		elif option=="dire_bm":
			self.y=0+pin_to_bm_y
			self.z=0+pin_to_bm_z
			return 1

    		elif option=="hfm_bm":
			self.y=6300+pin_to_bm_y
			self.z=0+pin_to_bm_z
			return 1

    		elif option=="vfm_bm":
			self.y=0+pin_to_bm_y
			self.z=79800+pin_to_bm_z
			return 1

    		elif option=="both_bm":
    			self.y=6300+pin_to_bm_y
    			self.z=79800+pin_to_bm_z
			return 1

    		else :
			self.y=-1
			self.z=-1
			return 0

	def move(self):
		print "Parameters: Moving stage to (x,y)=(%5d, %5d)\n"%(self.y,self.z)
		if self.y!=-1 and self.z!=-1:
			self.stage_y.move(self.y)
			self.stage_z.move(self.z)
		else:
			print "Pulse value is wrong"

	def monDirPIN(self):
		self.setPulse("dire_pin")
		self.move()

	def monVFMPIN(self):
		self.setPulse("vfm_pin")
		self.move()

	def monBothPIN(self):
		self.setPulse("both_pin")
		self.move()

if __name__=="__main__":
	host = '172.24.242.41'
	port = 10101
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host,port))

	mu=MirrorTuneUnit(s)
	mu.monVFMPIN()

	s.close()
