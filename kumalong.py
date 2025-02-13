import socket
import time
import datetime
import sys,os
import numpy

# My library
import Morning

class KUMAtune :
	def __init__(self):
		bglogname="TTT"
		basedir="/isilon/BL32XU/BLsoft/Logs/"
		# Beam position log
		self.bplogname="/isilon/BL32XU/BLsoft/Logs/beam.log"
		self.isInit=False

	def time_now(self):
		strtime=datetime.datetime.now().strftime("%H:%M:%S")
		return strtime

	def date_now(self):
		strtime=datetime.datetime.now().strftime("%Y%m%d-%H%M")
		return strtime

	def today(self):
		strtime=datetime.datetime.now().strftime("%Y%m%d")[2:]
		return strtime

	def time_str(self):
		strtime=datetime.datetime.now().strftime("%H%M")
		return strtime

	def beforeTune(self):
		# Setting for logfile
		self.dirname="/isilon/BL32XU/BLsoft/Logs/%s/"%(self.today())
		try:
        		os.stat(self.dirname)
		except:
        		os.mkdir(self.dirname)

		# Setting for logfile
		self.dirname="/isilon/BL32XU/BLsoft/Logs/%s/%s/"%(
			self.today(),self.time_str())
		try:
        		os.stat(self.dirname)
		except:
        		os.mkdir(self.dirname)

		self.isInit=True

	def autoTune(self,flag_needle=True):
		if self.isInit==False:
			self.beforeTune()

		mng=Morning.Morning(self.dirname)

		# Beam position log
		# KUMA should not write the beam position log file
		# Deleted 140616 by K.Hirata from Morning Tune
		# bplog=open(self.bplogname,"aw")

		# TCS aperture should be set to 0.1mm sq
		mng.setTCSapert(0.1,0.1)

		# Morning log file
		tstr=datetime.datetime.now().strftime("%Y-%m-%d-%H%M")
		fname="%s/MT_%s.dat"%(self.dirname,tstr)
		logf=open(fname,"w")

		#######################
		# Evacuate needle or pin
		#######################
		if flag_needle==True:
			sx,sy,sz=mng.evacNeedle(15)

		# Scintillator set position
		mng.prepBC()
		# Attenuator 1000um for 12.3984 keV 0.1 mm TCS apert
		mng.setAtt(1000)

		#######################
		# Wait for 60 sec
		#######################
		print "Waiting for thermal equilibrium of scintillator stage"
		time.sleep(60.0)

		# Open shutter
		mng.prepScan()

		# ST-YZ tune
		ini_sty,curr_sty,ini_stz,curr_stz=mng.stageYZtuneCapture()
		dy=(curr_sty-ini_sty)*1000.0 #[um]
		dz=(curr_stz-ini_stz)*1000.0 #[um]
		logf.write("%10s %10s Final Y=%10.4f Z=%10.4f (Dy,Dz)=(%5.2f,%5.2f)[um]\n"%(
			self.time_now(),"St-YZ tune",curr_sty,curr_stz,dy,dz))
		logf.flush()

		picy,picz=mng.doCapAna("confirm")
		#mng.saveBP(picy,picz)
		logf.write("%10s %10s code (Y,Z) = (%5d,%5d)\n"%(self.time_now(),"BeamCen",picy,picz))
		logf.flush()

		# Finish (remove beam monitor)
		mng.finishBC()

		# Collimator scan
		mng.colliScan()

		# Finish tuning
		mng.finishExposure()

		# Gonio move
		if flag_needle==True:
			mng.moveXYZmm(sx,sy,sz)

		# Making dynamic table & re-link bl41xu.conf to the newest one
		# Obsoleted currently 140616 0:20 K.Hirata
		# Because BSS tuning with BL41XU style is not useable in this mode
        	#mng.makeDynamic()
        	#print "Dynamic table for BSS has been updated!"
        	#print "Remember to restart BSS!"
        	#print "Remember to remove the tune-needle!"
	
		mng.allFin()
		logf.close()

if __name__=="__main__":

	#kt.beforeTune()

	for i in numpy.arange(0,10,1):
		kt=KUMAtune()
		kt.autoTune(False)
		time.sleep(3600)
