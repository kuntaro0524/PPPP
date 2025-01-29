import sys,os,math,cv2,socket,time,copy
from Mono import *
from MBS import *
from DSS import *
from ID import *
from TCS import *
from RingCurrent import *


class Asing():
	def __init__(self):
		host = '172.24.242.41'
		port = 10101
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.connect((host,port))

#		self.s=server

		self.id=ID(self.s)
		self.mono=Mono(self.s)
		self.tcs=TCS(self.s)
		self.mbs=MBS(self.s)
		self.dss=DSS(self.s)
		self.rc=RingCurrent(self.s)

	def isDump(self):
		# MBS check
		status_mbs=self.mbs.getStatus()
		status_dss=self.dss.getStatus()
		ir=self.rc.getRingCurrent()
		print "MBS Status =",status_mbs
		print "DSS_Status =",status_dss

		if ir < 90.0:
			print "Ring Current is low", ir
			return True
		if status_mbs!="open":
			print "MBS is not opened"
			return True
		if status_dss!="open":
			print "DSS is not opened"
			return True
		if self.id.isLocked!=0:
			print "ID is locked"
			return True
		return False

	def recover(self,wavelength):
		en=12.3984/wavelength
		gap=self.id.getE(en)

		ir=self.rc.getRingCurrent()
		if ir < 90.0:
			print "Ring Current is low", ir
			time.sleep(60)
			return False

		status_id=self.id.getGap()
		print "ID Gap =",status_id

		print "\ntry MBS open"
		if self.mbs.openTillOpen(wait_interval=60,ntrial=10)==False:
			print "MBS failed"
			return False
		print "\ntry ID change"
		if self.id.moveTillMove(gap,wait_interval=60,ntrial=10)==False:
			print "ID change failed"
			return False
		print "\ntry DSS open"
		if self.dss.openTillOpen(wait_interval=60,ntrial=10)==False:
			print "DSS open failed"
			return False

		# Tune dtheta1
		print "\nDTScan"
		prefix="temporal"
		self.mono.scanDt1PeakConfig(prefix,"DTSCAN_FULLOPEN",self.tcs)
		return True

if __name__=="__main__":
#	host = '172.24.242.41'
#	port = 10101 s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#	s.connect((host,port))

	asing=Asing()

	while True:
		if (asing.isDump() == True):
			print "Dumpped"
			print "Start Recovering"
			if asing.recover(1.0) == True:
				print "\nFinish Recoverd from Dump !!"
				print "wait dump"
				time.sleep(600)


