#!/bin/env python 
import sys
import socket
import time
from decimal import *

# My library
from Received import *
from Motor import *
from AnalyzePeak import *
from Count import *

class CameraStage:

	def __init__(self,server):
		self.s=server
    		self.cs=Motor(self.s,"bl_32in_st2_detector_1_y","pulse")
	
		# Camera stage
		self.prep_tune=-196000
		self.finish_tune=33

	def get(self):
		return self.cs.getPosition()[0]

	def move(self,pulse):
		self.cs.move(pulse)

	def prepTune(self):
		self.cs.move(self.prep_tune)

	def finishTune(self):
		self.cs.move(self.finish_tune)

if __name__=="__main__":
        host = '172.24.242.41'
        port = 10101
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host,port))

	cs=CameraStage(s)
	#cs.prepTune()
	cs.finishTune()

        s.close()
