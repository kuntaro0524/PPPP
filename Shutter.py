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
		tmp= self.s.recv(8000) # dummy buffer
		#self.query()

	def close(self):
		self.s.sendall(self.clsmsg)
		tmp= self.s.recv(8000) # dummy buffer
		#self.query()

	def query(self):
		self.s.sendall(self.qmsg)
		return self.s.recv(8000) # dummy buffer

	def isOpen(self):
		strstr=self.query()
		cutf=strstr[:strstr.rfind("/")]
		final=cutf[cutf.rfind("/")+1:]
		if final=="off":
			return 0
		else :
			return 1

if __name__=="__main__":
	#host = '192.168.163.1'
	host = '172.24.242.41'
        port = 10101
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host,port))

	#pin_ch=int(raw_input())

	shutter=Shutter(s)
	shutter.close()
	#sys.exit()
	cnt=0
	while(1):
		now=datetime.datetime.now()
		shutter.open()
		t1= shutter.isOpen()
		time.sleep(2.0)
		shutter.close()
		t2= shutter.isOpen()
		time.sleep(2.0)
		print "%s CNT:%d ON_FLAG=%s OFF_FLAG=%s"%(now,cnt,t1,t2)
		cnt+=1
