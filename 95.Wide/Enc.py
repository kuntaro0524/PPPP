#!/bin/env python 
import sys
import socket
import time

# My library
from Received import *
from Motor import *

#
class Enc:
	def __init__(self):
		print "Encoder class "

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
		print tmpstr

		# for y
		res="2/preset_%d"%sety
		com=root_com+res
        	self.s.sendall(com)
        	tmpstr=self.s.recv(8000) # dummy acquisition
		print tmpstr

		# for z
		res="3/preset_%d"%setz
		com=root_com+res
        	self.s.sendall(com)
        	tmpstr=self.s.recv(8000) # dummy acquisition
		print tmpstr

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
	#print enc.getXenc()
	#print enc.getYenc()
	#print enc.getZenc()
	#enc.resetEnc(36582,134664,-4934)
	print enc.getX()
	print enc.getY()
	print enc.getZ()
	enc.closePort()

