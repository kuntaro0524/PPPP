import os
import sys
sys.path.append("/isilon/BL32XU/BLsoft/PPPP/")

from AttFactor import *

class AnaBestLog:

	def __init__(self,filename):
		self.isInit=False
		self.att=AttFactor()
		self.filename=filename
		self.plan=[]
		self.predstat=[]
		self.other=[]
		#RESFLAG: Resolution limit is limited automatically by BEST=True
		self.rtndic={"RESLIM":4.0,"ANOFLAG":True,"EXPTIME":1.0,"STARTPHI":0.0,"NFRAMES":180,"ENDPHI":180.0,"WIDTH":1.0,"CL":100.0,"AL":1000.0,"RESFLAG":False,"WL":1.0}

	def extractBlock(self):
		self.lines=open(self.filename,"r").readlines()

		ncols=0
		# Skipping header
		for idx in range(0,len(self.lines)):
			line=self.lines.pop(0)
			if line.find("===")!=-1:
				break

		for idx in range(0,len(self.lines)):
			line=self.lines.pop(0)
			if line.find("===")!=-1:
				break
			else:
				self.plan.append(line)

		for idx in range(0,len(self.lines)):
			line=self.lines.pop(0)
			if line.find("===")!=-1:
				break
			else:
				self.predstat.append(line)

		for idx in range(0,len(self.lines)):
			line=self.lines.pop(0)
			if line.find("===")!=-1:
				break
			else:
				self.other.append(line)

		self.isInit=True
		return True

	def getDist(self):

		# Skipping non-required lines
		for idx in range(0,len(self.plan)):
			line=self.plan.pop(0)
			if line.find("Distance")!=-1:
				break
		# The next line is a spacer.
		self.plan.pop(0)

		#------------------------------------------------------------------
		 #N| Phi_start| N.of.images| Rot.width| Exposure|Distance| Overlap|
		 #-------------------------------------------------------------------
		  #1   105.00        43          2.25        0.31   443.0       No
		 #-------------------------------------------------------------------

		# The next line is an information
		return float(self.plan[0].split()[5])

	def getWave(self):
		for line in self.lines:
			if line.find("Wave")!=-1:
				return float(line.split()[2])

	def getDict(self):
		if self.isInit==False:
			self.extractBlock()

		for line in self.plan:
			if line.find("Resolution limit")!=-1:
				if line.find("limit is set")!=-1:
					self.rtndic["RESFLAG"]=True
					continue
				resol=round(float(line.strip().split(':')[1].split()[0]),2)

			if line.find("Anomalous data")!=-1:
				anoflag=line.strip().split(':')[1]

			if line.find("Phi_start - Phi_finish")!=-1:
				phirange=line.strip().split(":")[1]
				phistart=float(phirange.split()[0])

			if line.find("Total rotation range")!=-1:
				phitotal=round(float(line.strip().split(":")[1].split()[0]),1)

			if line.find("Total N.of images")!=-1:
				nframe=int(line.strip().split(":")[1])

			if line.find("Overal Completeness")!=-1:
				compl=float(line.strip().split(":")[1].replace("%",""))

			if line.find("Redundancy")!=-1:
				redun=float(line.strip().split(":")[1])

			if line.find("Total Exposure time")!=-1:
				exptot=float(line.strip().split(":")[1].split()[0])

		dist=self.getDist()
		wave=self.getWave()

	## Making dictionary
	## self.rtndic={"RESLIM":4.0,"ANOFLAG":True,"EXPTIME":1.0,"STARTPHI":0.0,"NFRAMES":180,"ENDPHI":180.0,"WIDTH":1.0,"CL":100.0,"AL":1000.0}
		self.rtndic["RESLIM"]=resol
		self.rtndic["ANOFLAG"]=anoflag
		self.rtndic["CL"]=dist

		## Oscillation range
		osc_width=round(phitotal/float(nframe),1)
		nframe=int(phitotal/osc_width)+1
		phitotal=float(nframe)*osc_width
		#print phitotal
		endphi=phistart+phitotal
		self.rtndic["STARTPHI"]=phistart
		self.rtndic["ENDPHI"]=round(endphi,1)
		self.rtndic["NFRAMES"]=int(nframe)

		# Exposure time
		exptime=round(exptot/float(nframe),1)
		self.rtndic["EXPTIME"]=exptime
		## End phi
		self.rtndic["WIDTH"]=osc_width
		# Suggested Attenuator for 1.0sec exposure
		althick=int(self.att.calcThickness(wave,exptime))
		if althick<0.0:
			self.rtndic["AL"]=0
		else:
			self.rtndic["AL"]=althick

		return self.rtndic

 #Resolution limit            : 4.06 Angstrom
 #Anomalous data              : No
 #Phi_start - Phi_finish      : 105.00 - 201.75
 #Total rotation range        : 96.75 degree
 #Total N.of images           : 43
 #Overal Completeness         : 95.4%
 #Redundancy                  : 4.19
 #R-factor (outer shell)      : 73.7% (  75.7%)
 #I/Sigma (outer shell)       : 2.1 (   2.0)
 #Total Exposure time         : 13.4 sec (0.004 hour)
 #Total Data Collection time  : 125.2 sec (0.035 hour)

if __name__=="__main__":
	bl=AnaBestLog(sys.argv[1])

	print bl.getDict()
