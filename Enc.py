#!/bin/env python 
import sys
import socket
import time
import datetime

# My library
from Received import *
from Motor import *

#
class Enc:
	def __init__(self):
		print "",

	def openPort(self):
		host = '192.168.163.107'
		port = 3665
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.connect((host,port))

	def closePort(self):
		self.s.close()

	def resetEnc(self,gx_pulse,gy_pulse,gz_pulse):
		# Setting for encoder value
		setx=int(gx_pulse)*10
		sety=int(gy_pulse)*10
		setz=int(gz_pulse)*10

		# Setting
		root_com="I/put/bl_32in_sc_counter"

		# for x
		res="1/preset_%d"%setx
		com=root_com+res
        	self.s.sendall(com)
        	tmpstr=self.s.recv(8000) # dummy acquisition
		#print tmpstr

		# for y
		res="2/preset_%d"%sety
		com=root_com+res
        	self.s.sendall(com)
        	tmpstr=self.s.recv(8000) # dummy acquisition
		#print tmpstr

		# for z
		res="3/preset_%d"%setz
		com=root_com+res
        	self.s.sendall(com)
        	tmpstr=self.s.recv(8000) # dummy acquisition
		#print tmpstr

	def str2value(self,value_str):
		ir=value_str.rfind("/")
		return float(value_str[ir+1:])/100.0 # [um]

	def getX(self):
		command="I/get/bl_32in_sc_encoderx/position"
        	self.s.sendall(command)
        	tmpstr=self.s.recv(8000) # dummy acquisition
		return self.str2value(tmpstr) # [um]

	def getY(self):
		command="I/get/bl_32in_sc_encodery/position"
        	self.s.sendall(command)
        	tmpstr=self.s.recv(8000) # dummy acquisition
		value=-self.str2value(tmpstr) # [um]
		return value

	def getZ(self):
		command="I/get/bl_32in_sc_encoderz/position"
        	self.s.sendall(command)
        	tmpstr=self.s.recv(8000) # dummy acquisition
		return self.str2value(tmpstr) # [um]

if __name__=="__main__":
	enc=Enc()
	enc.openPort()
	
	starttime=datetime.datetime.now()
	ndata=0
	# Kurikaeshi time
	total_time=float(sys.argv[1]) # sec
	time_HWlimit=0.05 # sec
	n_limit=int(total_time/time_HWlimit)

	print "%d times"%n_limit

	# List
	t_list=[]
	d_list=[]
	for i in range(n_limit):
		t_list.append(datetime.datetime.now())
		x=enc.getX()
		y=enc.getY()
		z=enc.getZ()
		d_list.append((x,y,z))

	print "Measurement finished!"
	print "Writing file...."

	ofile=open("enc.dat","w")
	for i in range(n_limit):
		t=t_list[i]
		time_from_start=t-starttime
		sec_part=float(time_from_start.seconds)
		sec_shousu=float(time_from_start.microseconds/1000000.0)
		dtime=sec_part+sec_shousu

		(x,y,z)=d_list[i]
		ofile.write("%8.5f %8.5f %8.5f %8.5f\n"%(dtime,x,y,z))

	ofile.close()
