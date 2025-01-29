import sys
import pylab
class ShelxLog:

	def __init__(self,filename):
		self.fname=filename
		self.isRead=False

	def readLines(self):
		iff=open(self.fname,"r")
		self.lines=iff.readlines()
		iff.close()
		self.isRead=True

	def choosePlotLine(self):
		if self.isRead==False:
			self.readLines()

		self.loglines=[]
		for line in self.lines:
			if line.find("Try")!=-1 and line.find("All")!=-1:
				self.loglines.append(line)

	def makePlotData(self):
		self.choosePlotLine()
		xdat=[]
		ydat=[]
		for line in self.loglines:
			xdat.append(float(line.split()[4]))
			ydat.append(float(line.split()[6].replace(",","")))

		px=pylab.array(xdat)
		py=pylab.array(ydat)

		pylab.plot(px,py,'.')
		pylab.xlabel("CC Weak")
		pylab.ylabel("CC All")
		#pylab.show()
		pylab.savefig("shelxd.png")

if __name__=="__main__":

	sl=ShelxLog(sys.argv[1])
	sl.makePlotData()
