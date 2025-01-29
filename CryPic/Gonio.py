#!/bin/env python 
import sys
import socket
import math

# My library
from Motor import *
#
class Gonio:
	def __init__(self,server):
		self.s=server
    		self.phi=Motor(self.s,"bl_32in_st1_gonio_1_omega","pulse")

		self.convertion=6667 # pulse-degree convertion [pulse/deg.]
		self.base=30.5 # home position of a spindle axis

	def getPhi(self):
		phi_pulse=self.phi.getPosition()
		phi_deg=float(phi_pulse[0])/float(self.convertion)+self.base
		phi_deg=round(phi_deg,3)
		return phi_deg

	def rotatePhi(self,phi):
		# put phi into the OK range
		if phi>720.0:
			phi=phi-720.0
		if phi<-720.0:
			phi=phi+720.0

		# deg -> pulse
		dif=phi*self.convertion

		# target pulse including the home position 
		orig=self.base*self.convertion
		pos_pulse=-(orig+-dif)

		# move the axis
		self.phi.move(pos_pulse)

if __name__=="__main__":
	host = '172.24.242.54' # BL41XU MS IP address
	port = 10101

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host,port))
	gonio=Gonio(s)

	print gonio.getPhi()
