#!/bin/env python 
import sys
import socket
import time
from decimal import *

# My library
from Received import *
from Motor import *
from AnalyzePeak import *

class Stage:

	def __init__(self,server):
		self.s=server
    		self.stage_z=Motor(self.s,"bl_32in_st2_stage_1_z","pulse")
    		self.stage_y=Motor(self.s,"bl_32in_st2_stage_1_y","pulse")

		self.p2v_z=15000.0
		self.p2v_y=10000.0

	def getZ(self):
		return self.stage_z.getPosition()[0]

	def getY(self):
		return self.stage_y.getPosition()[0]

	def moveZ(self,pulse):
		self.stage_z.move(pulse)

	def moveY(self,pulse):
		self.stage_y.move(pulse)

	def getZmm(self):
		pvalue=float(self.getZ())
		value=pvalue/self.p2v_z
		value=round(value,4)
		return value

	def getYmm(self):
		pvalue=float(self.getY())
		value=pvalue/self.p2v_y
		value=round(value,4)
		return value

	def moveYum(self,value):
		# um to mm
		vmm=value/1000.0
		# mm to pulse
		vp=int(vmm*self.p2v_y)

		# back lash[10um]

		# diff from current value
		if vp>=0.0:
			self.stage_y.relmove(vp)
		if vp<0.0:
			# current position [pulse]
			curr_yp=self.getY()

			# final position [pulse]
			final_yp=curr_yp+vp

			# back lash position[pulse] 10um
			bl_pulse=int(-0.01*self.p2v_y)
			bl_position=final_yp+bl_pulse
			self.stage_y.move(final_yp)
		
	def moveZum(self,value):
		# um to mm
		vmm=value/1000.0
		# mm to pulse
		vp=int(vmm*self.p2v_z)

		self.stage_z.relmove(vp)

if __name__=="__main__":
        host = '172.24.242.41'
        port = 10101
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host,port))

        stage=Stage(s)
	#print stage.getZmm(), stage.getYmm()

	#stage.moveZum(0.5)
	for i in range(0,5):
		stage.moveYum(1.0)
	for i in range(0,5):
		stage.moveYum(-1.0)

	#print stage.getZmm(), stage.getYmm()

        s.close()
