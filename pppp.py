from Stage import *
import sys
import datetime
import math
from MyException import *

class TestTest:
	def __init__(self,tcs,stage,capture,bm,shutter,att,mono,zoom,bs,cryo):
		self.tcs=tcs
		self.stage=stage
		self.cap=capture
		self.bm=bm
		self.shutter=shutter
		self.att=att
		self.mono=mono
		self.zoom=zoom
		self.bs=bs
		self.cryo=cryo


	#############################################
        	# Automatic stage tune #
	#############################################
	def doAutomatic(self,prefix):
        	# Center cross in [pix]
        	ceny=320
        	cenz=240

		# Tuning the gain of coax-camera
		try: 
			gain=self.cap.tuneGain()
		except MyException,ttt:
			raise MyException("gain tuning failed: %s\n"%ttt.args[0])
