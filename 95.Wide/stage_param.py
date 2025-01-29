#!/bin/env python 
import sys
import socket
import time
import datetime

# My library
from Mono import *
from FES import *
from ID import *
from TCS import *
from ExSlit1 import *
from AxesInfo import *
from File import *
from FixedPoint import  *
from Att import *
from SPACE import *
from MyException import *
from BM import *
from BS import *
from Stage import *
from Shutter import *
from Capture import *
from Gonio import *
from Colli import *
from Cryo import *
from CenteringNeedle import *
from Zoom import *
from MountPin import *

class AutoTune:

	def __init__(self):
		host = '172.24.242.41'
		port = 10101
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.connect((host,port))

		# Devices
		self.id=ID(self.s)
		self.mono=Mono(self.s)
		self.tcs=TCS(self.s)
		self.axes=AxesInfo(self.s)
		self.f=File("./")
		self.fixedp=FixedPoint(self.s)
		self.att=Att(self.s)
		self.space=SPACE()
		self.bm=BM(self.s)
		self.stage=Stage(self.s)
		self.shutter=Shutter(self.s)
		self.cap=Capture()
		self.colli=Colli(self.s)
		self.bs=BS(self.s)
		self.gonio=Gonio(self.s)
		self.cryo=Cryo(self.s)
		self.zoom=Zoom(self.s)
		
		# current directory
		self.curr_dir=self.f.getAbsolutePath()

	##############
        # Automatic stage tune #
	##############
	def stageTune(self):
                st=StageTune(self.stage,self.cap,self.bm,self.shutter,self.att,self.mono,self.zoom,self.bs)
		st.savePosition()
		st.diffLast()

if __name__=="__main__":
	at=AutoTune()
	at.stageTune()
