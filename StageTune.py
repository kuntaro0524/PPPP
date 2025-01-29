from Stage import *
import sys
import datetime
import math
from MyException import *

class StageTune:
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

	def prepTune(self):
		# Preparation of the diffractometer tools for stage tune
                # TCS slit is set to 0.1mm sq aperture
                #self.tcs.setApert(0.1,0.1)

                # Cryo off
                self.cryo.offFull() # using Nageppa

                # Zoom
                self.zoom_save=self.zoom.getPosition()
                self.zoom.go(0) # Maximum zoom

        	# Beam monitor on
        	self.bm.go(0)

		# Beam stopper on
        	self.bs.go(0)

		# Attenuator setting
		en=self.mono.getE()
		if en<=9.5:
			self.att.att0um()
		#elif en<=11.0:
			#self.att.att400um()
		elif en<=12.5:
			self.att.att1000um()
		else :
			self.att.att1500um()

		# Checking loop
		pCryo=0
		pZoom=0
		pBM=0
		pBS=0
		
		while(1):
			if self.cryo.isMoved()==False:
				pCryo=1
			if self.zoom.isMoved()==False:
				pZoom=1
			if self.bm.isMoved()==False:
				pBM=1
			if self.bs.isMoved()==False:
				pBS=1

			if pCryo==1 and pZoom==1 and pBM==1 and pBS==1:
				break
			else :
				print "waiting"
				print pCryo,pZoom, pBM,pBS
				time.sleep(2)

	def termTune(self):
		# Termination of the diffractometer tools for stage tune
        	# Beam monitor off
# 110530 by Y.K.
# 110618 motonimodosu 
        	self.bm.go(-75000)
#        	self.bm.go(-40000)

        	# Beam stopper
        	self.bs.goOff()

		# Cryo off
		self.cryo.goOff()

		# Zoom save position
		self.zoom.go(self.zoom_save)

        	# Attenuator setting
        	self.att.att0um()

		# Checking loop
		pCryo=0
		pZoom=0
		pBM=0
		pBS=0
		
		while(1):
			if self.cryo.isMoved()==False:
				pCryo=1
			if self.zoom.isMoved()==False:
				pZoom=1
			if self.bm.isMoved()==False:
				pBM=1
			if self.bs.isMoved()==False:
				pBS=1

			if pCryo==1 and pZoom==1 and pBM==1 and pBS==1:
				break
			else :
				print "waiting"
				print pCryo,pZoom,pBM,pBS
				time.sleep(2)

		# Reset shutter speed
		self.cap.setShutterSpeed(500)

	def savePosition(self):
		file="/isilon/BL32XU/BLtune/stage.dat"
		en=self.mono.getE()

		of=open(file,"a")
		date=datetime.datetime.now()

		curr_y=self.stage.getYmm()
		curr_z=self.stage.getZmm()

		diff_y,diff_z=self.diffLast()
		of.write("%s: %8.3f    %8.4f %8.4f ( %8.4f %8.4f )\n"%(date,en,curr_y,curr_z,diff_y,diff_z))

		# if the positional difference is larger than 20.0um
		if fabs(diff_y) >=20.0 or fabs(diff_z) >=20.0:
			raise MyException("Stage movement is too large z:%8.4f y:%8.4f\n"%(diff_z,diff_y))

		of.close()

	def diffLast(self):
		file="/isilon/BL32XU/BLtune/stage.dat"

		ifile=open(file,"r")
		lines=ifile.readlines()
		line=lines[len(lines)-1]
		#print line

		prev_y=float(line.split()[3])
		prev_v=float(line.split()[4])

		print "PREVIOUS %12.5f %12.5f\n" %(prev_y,prev_v)

		diff_y=1000.0*(prev_y-self.stage.getYmm())
		diff_z=1000.0*(prev_v-self.stage.getZmm())

		ifile.close()

		# return difference table parameters in [um]
		return diff_y, diff_z

	#############################################
        	# Automatic stage tune #
	#############################################
	def doAutomatic(self,prefix):
		# Preparing the tune
		self.prepTune()

        	# Center cross in [pix]
        	ceny=320
        	cenz=240

		# Shutter open
        	self.shutter.open()

		# Tuning the gain of coax-camera
		try: 
			gain=self.cap.tuneGain()
		except MyException,ttt:
			raise MyException("gain tuning failed: %s\n"%ttt.args[0])

        	for i in range(0,5):
                	print self.stage.getZmm(), self.stage.getYmm()
                	# caputure and analyze
               		y,z=self.cap.aveCenter(prefix)
	
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
