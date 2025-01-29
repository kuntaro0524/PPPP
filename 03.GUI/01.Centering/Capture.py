#!/bin/env python 
import sys
import socket
import time
import datetime
import os

# My library
from Received import *
from Organizer import *
from Dtheta import *
from FES import *
from ID import *
from TCS import *
from ExSlit1 import *
from AxesInfo import *
from Gonio import *

class Capture:
	
	def __init__(self):
		self.host='192.168.163.1'
		self.port = 10101
		self.open_sig=0
		self.isPrep=0
		self.user=os.environ["USER"]

	def prep(self):
	        command="ssh -l %s %s \"killall -9 videosrv\" &"%(self.user,self.host)
        	#print command
        	os.system(command)
	
        	command="ssh -X -l %s %s \"videosrv --artray\" &"%(self.user,self.host)
        	#print command
        	os.system(command)
	
        	time.sleep(1)
		self.isPrep=1

	def connect(self):
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.connect((self.host,self.port))
		self.open_sig=1

	def disconnect(self):
		if self.open_sig==1:
			self.open_sig=0
			self.isPrep=0
			self.s.close()

	def capture(self,filename):
		if self.isPrep==0:
			self.prep()
		if self.open_sig==0:
			self.connect()

		com1="get/bl_32in_st_1_video_grab/%s"%filename
		print com1
		self.s.sendall(com1)
		recbuf=self.s.recv(8000)
		print recbuf

		com2="put/bl_32in_st_1_video_connection/close"
		self.s.sendall(com1)
		recbuf=self.s.recv(8000)
		print recbuf

		#self.isPrep=0
		#self.open_sig=0
		#self.s.close()

        	#command="ssh -l hikima %s \"killall -9 videosrv\" &"%self.host
        	#print command
        	#os.system(command)


if __name__=="__main__":
	cap=Capture()
	cap.capture("/isilon/users/admin32/admin32/ppp.ppm")
