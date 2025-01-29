#!/bin/env python 
import sys
import socket
import time
import math
from pylab import *

# My library
from Gonio import *
from ID import *
from Mono import *
from TCS import *
from ConfigFile import *

class GonioBacklash:

	def __init__(self):
		host = '172.24.242.41'
		port = 10101
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((host,port))
	##	Device definition
		self.gonio=Gonio(s)
		self.conf=ConfigFile()
		self.f=File("./")

	def doScan(self,prefix,range,step,ntimes,phi):
		## 	PHI control
			self.gonio.rotatePhi(phi)
		## 	Gonio set position [mm]
			sx=0.0128
			sy=-15.1413
			sz=-0.4489
		
		
		### 	Starting position
			self.gonio.moveXYZmm(sx,sy,sz)
		
		## 	Preparing gonio information (reset encoder)
			self.gonio.prepScan()
		
		# 	X axis
		## 	Log file
			filename="%s_x.log"%prefix
			logf=open(filename,"w")
			for i in arange(0,ntimes,1):
				for dx in arange(-range,+range,step):
					nx=sx+dx
					self.gonio.moveXYZmm(nx,sy,sz)
					ex,ey,ez=self.gonio.getEnc()
		
					logf.write("IDEAL: %12.5f OBS: %12.5f\n"%(nx,ex))
					logf.flush()
				for dx in arange(+range,-range,-step):
					nx=sx+dx
					self.gonio.moveXYZmm(nx,sy,sz)
					ex,ey,ez=self.gonio.getEnc()
		
					logf.write("IDEAL: %12.5f OBS: %12.5f\n"%(nx,ex))
					logf.flush()
				logf.write("\n\n")
		
			logf.close()
		###################################################################################
		# 	Y axis
		## 	Log file
		### 	Starting position
			self.gonio.moveXYZmm(sx,sy,sz)
			filename="%s_y.log"%prefix
			logf=open(filename,"w")
		
			for i in arange(0,ntimes,1):
				for dy in arange(-range,+range,step):
					ny=sy+dy
					self.gonio.moveXYZmm(sx,ny,sz)
					ex,ey,ez=self.gonio.getEnc()
		
					logf.write("IDEAL: %12.5f OBS: %12.5f\n"%(ny,ey))
					logf.flush()
				for dy in arange(+range,-range,-step):
					ny=sy+dy
					self.gonio.moveXYZmm(sx,ny,sz)
					ex,ey,ez=self.gonio.getEnc()
		
					logf.write("IDEAL: %12.5f OBS: %12.5f\n"%(ny,ey))
					logf.flush()
				logf.write("\n\n")
			logf.close()
		
		###################################################################################
		# 	Z axis
		## 	Log file
		####	Starting position
			self.gonio.moveXYZmm(sx,sy,sz)
			filename="%s_z.log"%prefix
			logf=open(filename,"w")
			for i in arange(0,ntimes,1):
				for dz in arange(-range,+range,step):
					nz=sz+dz
					self.gonio.moveXYZmm(sx,sy,nz)
					ex,ey,ez=self.gonio.getEnc()
		
					logf.write("IDEAL: %12.5f OBS: %12.5f\n"%(nz,ez))
					logf.flush()
		
				for dz in arange(+range,-range,-step):
					nz=sz+dz
					self.gonio.moveXYZmm(sx,sy,nz)
					ex,ey,ez=self.gonio.getEnc()
			
					logf.write("IDEAL: %12.5f OBS: %12.5f\n"%(nz,ez))
					logf.flush()
				logf.write("\n\n")
			logf.close()
	
if __name__=="__main__":

	gb=GonioBacklash()


##	Scan step
	range=0.005
	step=0.001
	ntimes=5

	phi_list=[0,180,90,270]

	for phi in phi_list:
		prefix="phi%d"%phi	
		gb.doScan(prefix,range,step,ntimes,phi)
