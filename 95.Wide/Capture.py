#!/bin/env python 
import sys
import socket
import time
import datetime
import os

# My library
from BeamCenter import *

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
	
		time.sleep(1.0)
        	command="ssh -X -l %s %s \"videosrv --artray\" &"%(self.user,self.host)
        	#print command
        	os.system(command)
	
		self.isPrep=1
		time.sleep(5.0)

	def connect(self):
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.connect((self.host,self.port))
		self.open_sig=1

	def disconnect(self):
		if self.open_sig==1:
			self.open_sig=0
			self.isPrep=0
			self.s.close()

	def setBright(self,bright):
		# set brightness
		com_bright="put/bl_32in_st_1_video_brightness/%d"%bright
		self.s.sendall(com_bright)
		recbuf=self.s.recv(8000)
		print recbuf

	def setCross(self):
		com1="put/video_cross/on"
		self.s.sendall(com1)
		recbuf=self.s.recv(8000)
		print recbuf

	def unsetCross(self):
		com1="put/video_cross/off"
		self.s.sendall(com1)
		recbuf=self.s.recv(8000)
		print recbuf

	def capture(self,filename,bright=7800):
		if self.isPrep==0:
			self.prep()
		if self.open_sig==0:
			self.connect()

		# unset cross
		self.unsetCross()

		# set brightness
		self.setBright(bright)
		# capture the figure
		com1="get/bl_32in_st_1_video_grab/%s"%filename
		self.s.sendall(com1)
		recbuf=self.s.recv(8000)

		# set cross
		self.setCross()

		print recbuf

        def captureBM(self,filename):
                # Capture before fixed point scan
                self.capture(filename,5000)

                # Acquire beam center position from PPM file
                try :
                        bc=BeamCenter(filename)
                        x,y=bc.find()

                except MyException,ttt:
                        print ttt.args[0]
			raise MyException("captureBM failed: %s\n"%ttt.args[0])

                return x,y

if __name__=="__main__":
	cap=Capture()
	cap.capture("/isilon/BL32XU/BLsoft/PPPP/ppp.ppm")

	#cap.captureBM("/isilon/BL32XU/BLsoft/PPPP/ppp.ppm",12.398)
	#cap.captureManma()
