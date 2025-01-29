#!/bin/env python 
import errno
import sys
import socket
import time
import datetime
import os
import numpy
from socket import error as socket_error

class Capture:
	def __init__(self):
		self.host='172.30.102.1' # for SACLA videosrv 150614 modified
		self.port = 10101
		self.open_sig=0
		self.isPrep=0
		self.user=os.environ["USER"]

	def connect(self):
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			self.s.connect((self.host,self.port))
			self.isPrep=1
		except socket_error as serr:
			return False

		print "Connection established"
		return True

	def disconnect(self):
		if self.isPrep==1:
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
		#print recbuf

	def unsetCross(self):
		com1="put/video_cross/off"
		self.s.sendall(com1)
		recbuf=self.s.recv(8000)
		#print recbuf

		# unset cross
		self.unsetCross()

		# 140528
		self.setShutterSpeed(speed)
		time.sleep(0.1)

		com1="get/bl_32in_st_1_video_grab/%s"%filename
		self.s.sendall(com1)
		recbuf=self.s.recv(8000)
		# set cross
		self.setCross()

	def captureWithCross(self,filename,bright=15):
		if self.isPrep==0:
			self.connect()

		# set cross
		self.setCross()

		self.setGain(bright)
		time.sleep(0.5)

		# capture the figure
		print "Obtaining %s from videosrv"%filename
		com1="get/bl_32in_st_1_video_grab/%s"%filename
		self.s.sendall(com1)
		recbuf=self.s.recv(8000)

		print recbuf

	def capture(self,filename,bright=7800,speed=600):
		if self.isPrep==0:
			self.connect()

		com1="get/bl_32in_st_1_video_grabnocross/%s"%filename
		com1="get/video_grabnocross/%s"%filename
		com1="get/grab/%s"%filename
		print com1
		self.s.sendall(com1)
		recbuf=self.s.recv(8000)
		print "debug::",recbuf

	def setBinning(self, binning):
		com1="put/video_binning/%d"%binning
		self.s.sendall(com1)
		recbuf=self.s.recv(8000)
		print "debug::",recbuf

	def getBinning(self):
		com1="get/video_binning/"
		self.s.sendall(com1)
		recbuf=self.s.recv(8000)
		print "debug::",recbuf
		sp = recbuf.split("/")
		if len(sp) == 5:
			return int(sp[-2])

	def setShutterSpeed(self,speed):
	        command="ssh -l %s %s \"echo %d > /sys/class/video4linux/video0/shutter_width\""%(self.user,self.host,speed)
		#print "command=%s"%command
		#time.sleep(5)
        	os.system(command)

	def setGain(self,gain):
	        command="ssh -l %s %s \"echo %d > /sys/class/video4linux/video0/gain\""%(self.user,self.host,gain)
		#print "command=%s"%command
        	os.system(command)

        def captureBM(self,filename,gain=5000):
                # Capture before fixed point scan
                self.capture(filename,gain)

                # Acquire beam center position from PPM file
                try :
                        bc=BeamCenter(filename)
                        x,y=bc.find()

                except MyException,ttt:
                        print ttt.args[0]
			raise MyException("captureBM failed: %s\n"%ttt.args[0])

                return x,y

        def captureFast(self,filename,bright=12):
		if self.isPrep==0:
			self.prep()
		if self.open_sig==0:
			self.connect()
	
		self.setShutterSpeed(50)

                # Capture before fixed point scan
		print "FILE:%s\n"%filename
                self.capture(filename,bright)

                # Acquire beam center position from PPM file
		time.sleep(1)
                try :
                        bc=BeamCenter(filename)
                        x,y=bc.find()

                except MyException,ttt:
                        print ttt.args[0]
			raise MyException("captureBM failed: %s\n"%ttt.args[0])

                return x,y

	def captureAndCheck(self,ofile,gain):
		print "BRIGHT=%d"%gain
		self.capture(ofile,gain)
        	bc=BeamCenter(ofile)
        	nsat=bc.countSaturated()

		return nsat

	def tuneShutter(self,bright=7800):
                tmpfile="/isilon/BL32XU/BLsoft/PPPP/tmp.ppm"

		curr_speed=1200
		self.setShutterSpeed(curr_speed)

		nsat=self.captureAndCheck(tmpfile,bright)


        	while(1):
                	for i in range(0,5):
                        	if nsat > 1500:
                                	curr_speed-=1000
                        	elif nsat < 1000:
                                	curr_speed+=1000
	
                        	if curr_speed<0:
                                	curr_speed=0

				self.setShutterSpeed(curr_speed)
                        	nsat=self.captureAndCheck(tmpfile,bright)
				print "Sat:%5d\n"%nsat

				if nsat < 1500 and nsat > 1000:
					break

                	for i in range(0,5):
                        	if nsat > 1500:
                                	curr_speed-=500
                        	elif nsat < 1000:
                                	curr_speed+=500
	
                        	if curr_speed<0:
                                	curr_speed=0

				self.setShutterSpeed(curr_speed)
                        	nsat=self.captureAndCheck(tmpfile,bright)
				print "Sat:%5d\n"%nsat

				if nsat < 1500 and nsat > 1000:
					break

                	for i in range(0,5):
                        	if nsat > 1500:
                                	curr_speed-=100
                        	elif nsat < 1000:
                                	curr_speed+=100
	
                        	if curr_speed<0:
                                	curr_speed=0

				self.setShutterSpeed(curr_speed)
                        	nsat=self.captureAndCheck(tmpfile,bright)
				if nsat < 1500 and nsat > 1000:
					break
				print "Sat:%5d\n"%nsat


			return curr_speed

	def tuneGain(self,default_gain=120,default_shutter=1300):
                tmpfile="/isilon/BL32XU/BLsoft/PPPP/tmp.ppm"

		nsat=self.captureAndCheck(tmpfile,default_gain)
		self.setShutterSpeed(default_shutter)

		# Is there a beam on the captured ppm?
                bc=BeamCenter(tmpfile)
                summed_value=bc.getSummed()

		print "SUMMED:%d\n"%summed_value
		if summed_value==0:
			raise MyException("caputured image has no beam profile")

		#if nsat>10000:
			#raise MyException("captureBM failed: Beam is too intense")

		gain=default_gain

		if nsat < 1500 and nsat > 1000:
			return gain

                for i in range(0,5):
                       	if nsat > 1500:
                               	gain-=20
                       	elif nsat < 1000:
                               	gain+=20
	
                       	if gain<0:
                               	gain=8

                       	nsat=self.captureAndCheck(tmpfile,gain)
			print "Saturated:%5d\n"%nsat

			if nsat < 1500 and nsat > 1000:
				return gain

                for i in range(0,5):
                       	if nsat > 1500:
                               	gain-=10
                       	elif nsat < 1000:
                               	gain+=10

                       	if gain<0:
                               	gain=8

                       	nsat=self.captureAndCheck(tmpfile,gain)
			print "Saturated:%5d\n"%nsat

			if nsat < 1500 and nsat > 1000:
				return gain

               	for i in range(0,5):
                       	if nsat > 1500:
                               	gain-=3
                       	elif nsat < 1000:
                               	gain+=3
	
                       	if gain<0:
                               	gain=8

                       	nsat=self.captureAndCheck(tmpfile,gain)
			if nsat < 1500 and nsat > 1000:
				return gain
			print "Saturated:%5d\n"%nsat

		if gain < 0 :
			gain=8

		return int(gain)

	def aveCenter(self,prefix,gain,nave=5,speed=4000):
                totx=toty=0

                for i in range(0,nave):
                        filename="%s_%03d.ppm"%(prefix,i)
			self.captureWithSpeed(filename,speed)
			time.sleep(0.5)
                        pp=BeamCenter(filename)
                        #x,y=pp.find()
                        x,y=pp.findRobust()

                        totx+=x
                        toty+=y

		cenx=totx/float(nave)
		ceny=toty/float(nave)

		return cenx,ceny

if __name__=="__main__":
	cap=Capture()
	
	print cap.disconnect()
	print cap.connect()
	#print cap.getBinning()
	cap.capture("/home/bluser/k.ppm")
	cap.disconnect()
