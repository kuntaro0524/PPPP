import sys

class LogFile:

	def __init__(self,filename):
		self.filename=filename
		self.lines=[]
		self.isRead=False

	def storeLines(self):
		fin=open(self.filename,"r")
		self.lines=fin.readlines()
		fin.close()
		self.isRead=True

	def getLines(self):
		if self.isRead==False:
			self.storeLines()
		return self.lines

if __name__=="__main__":
	
	lf=LogFile(sys.argv[1])
	print lf.getLines()
