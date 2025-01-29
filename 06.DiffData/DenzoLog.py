import sys
sys.path.append("/isilon/BL32XU/BLsoft/PPPP/")

from LogFile import *

class DenzoLog(LogFile):

	def __init__(self,filename):
		LogFile.__init__(self,filename)
		# denzo.log file 
		self.filename=filename
		self.results=[]

	def test(self):
		return self.getLines()

	def findPenalty(self):
		for line in self.getLines():
			if (line.find("primitive cubic")!=-1):
				self.results.append(line)
			elif (line.find("I centred cubic")!=-1):
				self.results.append(line)
			elif (line.find("primitive rhombohedral")!=-1):
				self.results.append(line)
			elif (line.find("primitive hexagonal")!=-1):
				self.results.append(line)
			elif (line.find("primitive tetragonal")!=-1):
				self.results.append(line)
			elif (line.find("I centred tetragonal")!=-1):
				self.results.append(line)
			elif (line.find("primitive orthorhombic")!=-1):
				self.results.append(line)
			elif (line.find("C centred orthorhombic")!=-1):
				self.results.append(line)
			elif (line.find("I centred orthorhombic")!=-1):
				self.results.append(line)
			elif (line.find("F centred orthorhombic")!=-1):
				self.results.append(line)
			elif (line.find("primitive monoclinic")!=-1):
				self.results.append(line)
			elif (line.find("C centred monoclinic")!=-1):
				self.results.append(line)
			else:
				continue

		return self.results

if __name__=="__main__":
	dl=DenzoLog("./denzo.log")
	#print dl.test()
	print dl.findPenalty()
