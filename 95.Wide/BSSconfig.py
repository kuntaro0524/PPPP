from MyException import *

class BSSconfig:
	def __init__(self):
		self.file="/isilon/blconfig/bl32xu/bss/bss.config"
		self.isRead=False
		self.isPrep=False

	def storeLines(self):
		ifile=open(self.file,"r")
		self.lines=ifile.readlines()
		
		ifile.close()
		self.isRead=True

	def get(self,confstr):
		if self.isRead==False:
			self.storeLines()

		isFound=False
		for line in self.lines:
			# skip "#" character
			if line[0]=="#":
				continue
			if line.find(confstr)!=-1:
				isFound=True
				fstr=line
				break

		# check if the string was found
		if isFound==False:
			raise MyException("config string was not found.")

		# strip after "#"
		if fstr.rfind("#")!=-1:
			fstr=fstr[:fstr.rfind("#")-1]

		# ":" treatment
		return fstr[fstr.rfind(":")+1:]

	def getValue(self,confstr):
		strvalue=self.get(confstr)
		#print strvalue
		return float(strvalue)

	def readEvacuate(self):
		try:
			self.cryo_on=self.getValue("Cryostream_1_On_Position")
			self.cryo_off=self.getValue("Cryostream_1_Off_Position")
			self.colli_on=self.getValue("Collimator_1_On_Position")
			self.colli_off=self.getValue("Collimator_1_Off_Position:")
			self.bs_on=self.getValue("Beam_Stop_1_On_Position")
			self.bs_off=self.getValue("Beam_Stop_1_Off_Position:")

		except MyException,ttt:
			print ttt.args[0]

		self.isPrep=True

	def getCmount(self):
		if self.isPrep==False:
			self.readEvacuate()
		return self.mountx,self.mounty,self.mountz

	def getCryo(self):
		if self.isPrep==False:
			self.readEvacuate()
		return self.cryo_on,self.cryo_off

	def getBS(self):
		if self.isPrep==False:
			self.readEvacuate()
		return self.bs_on,self.bs_off

	def getColli(self):
		if self.isPrep==False:
			self.readEvacuate()
		return self.colli_on,self.colli_off

if __name__=="__main__":
	bssconf=BSSconfig()
	
	
	try:
		print bssconf.getCmount()
		print bssconf.getCryo()
		print bssconf.getColli()
		print bssconf.getBS()

	except MyException,ttt:
		print ttt.args[0]

