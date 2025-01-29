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



        	for i in range(0,5):
                	print self.stage.getZmm(), self.stage.getYmm()
                	# caputure and analyze
               		y,z=self.cap.aveCenter(prefix,gain)
	
                	# diff x,y
                	dy=y-ceny
                	dz=z-cenz
	
                	# pixel to micron [um/pixel] in high zoom
                	p2u_z=7.1385E-2
                	p2u_y=9.770E-2
	
                	z_move=-dz*p2u_z
                	y_move=dy*p2u_y
	
                	print "Z: %8.4f [um]"%z_move
                	print "Y: %8.4f [um]"%y_move

			if math.fabs(z_move) < 0.5 and math.fabs(y_move) < 0.5:
				print "Tune is enough!!\n"
				break
			if math.fabs(z_move) > 500 or math.fabs(y_move) > 500:
				raise MyException("Stage movement is too large z:%8.4f y:%8.4f\n"%(z_move,y_move))
	
                	#print z_move
                	self.stage.moveZum(z_move)
                	self.stage.moveYum(y_move)
			time.sleep(3)

		# Save position
		try:
			self.savePosition()
		except MyException,ttt:
			raise MyException("savePosition() failed: %s\n"%ttt.args[0])

		# Shutter close
        	self.shutter.close()

		# Terminating the tune
		self.termTune()
