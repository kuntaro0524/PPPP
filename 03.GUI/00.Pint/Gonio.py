#!/bin/env python 
import sys
import socket
import time
import math
from pylab import *

# My library
from Organizer import *
from PeakFWHM import *
from AnalyzeData import *
from File import *

#
class Gonio:

	def __init__(self,server,cnt_ch):
		self.cnt_ch=cnt_ch
		self.s=server
    		self.goniox=Organizer(self.s,"bl_32in","st2_gonio_1","x")
    		self.gonioy=Organizer(self.s,"bl_32in","st2_gonio_1","y")
    		self.gonioz=Organizer(self.s,"bl_32in","st2_gonio_1","z")
    		self.phi=Organizer(self.s,"bl_32in","st2_gonio_1","phi")

		self.convertion=6667
		self.base=210.0

	def getPhi(self):
		phi_pulse=self.phi.getPosition()
		print phi_pulse
		phi_deg=float(phi_pulse[0])/float(self.convertion)+self.base

		phi_deg=round(phi_deg,3)

		return phi_deg

	def movePint(self,value_um):
		# Current status
		curr_phi=self.getPhi()
		print "PHI:%12.5f" % curr_phi
		curr_phi=math.radians(curr_phi)
                curr_x=int(self.getX()[0])
                curr_z=int(self.getZ()[0])

		# unit [um]
		move_x=value_um*math.cos(curr_phi)
		move_z=value_um*math.sin(curr_phi)

		# marume [um]
		move_x=round(move_x,5)
		move_z=round(move_z,5)

		# marume value[pulse]
		move_x=int(move_x*10)
		move_z=int(move_z*10)

		#print move_x,move_z

		# final position
		final_x=int(curr_x)+move_x
		final_z=int(curr_z)+move_z

		print "Current X,Z[pulse]= %12d %12d" %(final_x,final_z)

		self.moveXZ(final_x,final_z,"pulse")

		#print move_x,move_z
		#return move_x,move_z

	def rotatePhi(self,phi):
		convertion=6667 #deg2pulse
		dif=phi*convertion

		base=210
		
		orig=base*convertion
		pos_pulse=-(orig+-dif)

		self.phi.move(pos_pulse,"pulse")
		print pos_pulse

	def scan2D(self,prefix,zrange,yrange,ch,time):
		# output file
		ofile=prefix+"_gonio2D.scn"
		of=open(ofile,"w")

		# zrange, yrange unit[um]
		start_i=0
		end_i=1
		step_i=2

		# loop
		for zd in arange(zrange[start_i],zrange[end_i],zrange[step_i]):
			zd_pulse=int(zd*10)
			self.moveZ(zd_pulse,"pulse")

			for yd in arange(yrange[start_i],yrange[end_i],yrange[step_i]):
				yd_pulse=int(yd*10)
				self.moveY(yd_pulse,"pulse")

				# get Count at each position
				cnt=self.goniox.getCount(ch,time)

				of.write("%8.5f %8.5f %8d\n"%(zd,yd,cnt))
				of.flush()
			of.write("\n\n")

	def getX(self):
		return self.goniox.getPosition()

	def getY(self):
		return self.gonioy.getPosition()

	def getZ(self):
		return self.gonioz.getPosition()

	def moveZ(self,value,unit):
		self.gonioz.move(value,unit)

	def moveY(self,value,unit):
		self.gonioy.move(value,unit)

	def moveXZ(self,movex,movez,unit):
		self.goniox.move(movex,unit)
		self.gonioz.move(movez,unit)

	def move(self,x,y,z,unit):
		self.goniox.move(x,unit)
		self.gonioy.move(y,unit)
		self.gonioz.move(z,unit)

	def scanZ(self,ofile,start,end,step,time,unit):
		# Setting
    		maxvalue=self.gonioz.axisScan(ofile,start,end,step,self.cnt_ch,self.cnt_ch-1,time,unit)
		return(maxvalue)

	def scanY(self,ofile,start,end,step,time,unit):
    		maxvalue=self.gonioy.axisScan(ofile,start,end,step,self.cnt_ch,self.cnt_ch-1,time,unit)
		return(maxvalue)

	def findCenter(self,ofile,start,end,step,time,unit):
		# Set step
    		maxvalue=self.gonioz.axisScan(ofile,start,end,step,self.cnt_ch,self.cnt_ch-1,time,unit)

		return(maxvalue)

if __name__=="__main__":
	host = '172.24.242.41'
	port = 10101
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host,port))
	gonio=Gonio(s,3)

	#value=float(raw_input())
	#gonio.movePint(value)

	file=File("./")
	dir=file.getAbsolutePath()
	
	savex=gonio.getX()[0]
	savey=gonio.getY()[0]
	savez=gonio.getZ()[0]

	index=0
	#for pint in arange(-10,10,1.0): # unit[um]
		#index+=1
		#print "pint=%5d\n"%pint
		#gonio.movePint(savex,savez,pint)
		#prefix="%02d"%index
	#	
		#file="%s/%s.ppm"%(dir,prefix)
		#print file
        	##cap.capture(file)
	#gonio.move(savex,savey,savez,"pulse")

	zrange=[-292,-1092,-100]
	yrange=[13329,14129,100]
	gonio.scan2D("TEST2",zrange,yrange,2,0.5)

	gonio.move(savex,savey,savez,"pulse")

	#cap.disconnect()

	# coordinates [Y,Z]
	#normal_position=[176400,-100]
	#vscan_position= [176400,-100]
	#hscan_position= [175000,-460]

	# move normal position
	#gonio.move(normal_position[0],normal_position[1],"pulse")

	# vertical scan
	#gonio.move(vscan_position[0],vscan_position[1],"pulse")
	#gonio.scanZ("gz",300,500,10,0.2,"pulse")

	#gonio.move(hscan_position[0],hscan_position[1],"pulse")
	#gonio.scanY("gy",172640,173040,10,0.2,"pulse")

	s.close()
