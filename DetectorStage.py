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

class DetectorStage:

	def __init__(self,server):
		self.s=server
    		self.sty=Motor(self.s,"bl_32in_st2_detector_1_y","pulse")
		self.evacuate_position=-196000
		self.in_position=33

	def getY(self):
		return self.sty.getPosition()[0]

	def moveY(self,pulse):
		self.sty.move(pulse)

	def evacuate(self):
		self.moveY(self.evacuate_position)

	def moveToOrigin(self):
		self.moveY(self.in_position)

if __name__=="__main__":
        host = '172.24.242.41'
        port = 10101
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host,port))

        stage=DetectorStage(s)
	yyy=stage.evacuate()
        s.close()
