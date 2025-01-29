#!/bin/env python 
import sys
import socket
import time

# My library
from TCS import *

mag_fac_vert=26.0
mag_fac_hori=40.0

class SetBeamSize:
	def __init__(self):
		host = '172.24.242.41'
		port = 10101
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.connect((host,port))

	def setSize(self,size_sq):

		if size_sq<0.5 or size_sq >= 7.0 :
			return -1

		# TC slit size [um]
		vert_width=size_sq*mag_fac_vert/1000.0
		hori_width=size_sq*mag_fac_hori/1000.0

		print "V:%8.3f H:%8.3f" %(vert_width, hori_width)

		#tcs.setApert(aperture,aperture)
		self.s.close()
		return 1

if __name__=="__main__":
	bs=BeamSizer()

	bs.setSize(5)
