#!/bin/env python 
import sys
import socket
import time
import datetime
#from Count import *

# My library

class Shutter:
	def __init__(self,server):
		self.s=server
		self.openmsg="put/bl_32in_st2_shutter_1/on"
		self.clsmsg="put/bl_32in_st2_shutter_1/off"
		self.qmsg="get/bl_32in_st2_shutter_1/status"

	def open(self):
		self.s.sendall(self.openmsg)
		print self.s.recv(8000) # dummy buffer
		#self.query()

	def close(self):
		self.s.sendall(self.clsmsg)
		print self.s.recv(8000) # dummy buffer
		#self.query()

	def query(self):
		self.s.sendall(self.qmsg)
		print self.s.recv(8000) # dummy buffer


if __name__=="__main__":
	host = '172.24.242.41'
        port = 10101
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host,port))

	#pin_ch=int(raw_input())

	shutter=Shutter(s)
	#cnt=Count(s,pin_ch)

	shutter.open()
	#print "OPEN"
	#time.sleep(5)
	#shutter.close()

	#while (1):
		#time.sleep(3)
		#shutter.close()
		#time.sleep(3)
		#shutter.open()
	#print cnt.getPIN(4)
	#shutter.close()
