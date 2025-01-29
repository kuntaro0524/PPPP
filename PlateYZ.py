#!/bin/env python 
import sys
import socket
import time
import datetime 

# My library
from Received import *
from Motor import *
from BSSconfig import *

#
class PlateYZ:
	def __init__(self,server):
		self.s=server
    		self.plate_y=Motor(self.s,"bl_32in_st2_plate_1_y","pulse")
    		self.plate_z=Motor(self.s,"bl_32in_st2_plate_1_z","pulse")
		
		self.isInit=False


        def moveZ(self,pls):
                self.plate_z.move(pls)

        def moveY(self,pls):
                self.plate_y.move(pls)

	def getZ(self):
		return self.plate_z.getPosition()

	def getY(self):
		return self.plate_y.getPosition()


if __name__=="__main__":
	host = '172.24.242.41'
	port = 10101

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host,port))

	plate=PlateYZ(s)

	plate.getY()
	plate.getZ()

	s.close()
