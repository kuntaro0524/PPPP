#!/bin/env python 
import sys
import socket
import time

# My library
from ExSlit2 import *

#####################################
#	def fullOpen(self):
#	def setUpper(self,position):
#	def setLower(self,position):
#	def setRing(self,position):
#	def setHall(self,position):
#	def setSize(self,v_apert,h_apert):
#       def scanV(self,prefix,start,end,step,cnt_ch1,cnt_ch2,time):
#       def scanH(self,prefix,start,end,step,cnt_ch1,cnt_ch2,time):
#####################################

if __name__=="__main__":
	host = '172.24.242.41'
	port = 10101
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host,port))

	slit2=ExSlit2(s)

	# Slit size
	if len(sys.argv)!=3:
		print "Usage: program V H"

	else:
		vsize=int(sys.argv[1])
		hsize=int(sys.argv[2])

	# slit aperture
	slit2.setSize(vsize,hsize)
	
	s.close()
