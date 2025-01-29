import math

class Scalepack:

	def __init__(self,filename):
		self.filename=filename
		self.eqref=[]

	def read(self):
		ifile=open(self.filename,"r")
		self.lines=ifile.readlines()

	def store(self):
		# first line
		line=self.lines[0]
		params=self.split(line)
		sh,sk,sl=self.getEqHKL(params)

		# Eq list
		eqlist=[]
		# Main loop
		for line in self.lines:
			params=self.split(line)
			oh,ok,ol=self.getEqHKL(params)
			#print sh,sk,sl,oh,ok,ol
			if oh==sh and ok==sk and ol==sl:
				img=self.getImgNum(params)
				I,sigI=self.getIsig(params)
				#print oh,ok,ol,img,I,sigI
				eqlist.append([oh,ok,ol,img,I,sigI])
			else:	
				#print eqlist
				self.eqref.append(eqlist)
				eqlist=[]
				#print "######"
				sh=oh
				sk=ok
				sl=ol
				#print "NEW:%d %d %d\n"%(sh,sk,sl)
				img=self.getImgNum(params)
				I,sigI=self.getIsig(params)
				eqlist.append([oh,ok,ol,img,I,sigI])

	def getEqHKL(self,params):
		return int(params[3]),int(params[4]),int(params[5])

	def getImgNum(self,params):
		return int(params[6])

	def getIsig(self,params):
		return float(params[10]),float(params[11])

	def split(self,line):
		params=line.split()
		return params

	def printData(self):
		neq=len(self.eqref)
		for i in range(0,neq):
			ninc=len(self.eqref[i])
			for j in range(0,ninc):
				print self.eqref[i][j]
			print "######"

if __name__=="__main__":
	scl=Scalepack("original.sca")
	scl.read()
	scl.store()
	scl.printData()
