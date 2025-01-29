import os,sys,math

class AnaXSCALELP:
	def __init__(self,xscalelp):
		self.xscalelp=xscalelp
		self.isInit=False
		self.isList=False

	def init(self):
		self.lines=open(self.xscalelp,"r").readlines()
		self.isInit=True

	def listInput(self):
		if self.isInit==False:
			self.init()

		self.input_files=[]
		for line in self.lines:
			if line.rfind("INPUT_FILE=")!=-1:
				add_line=line.replace("INPUT_FILE=","")
				self.input_files.append(add_line)

		self.isList=True
		return self.input_files

	def getDataname(self,delim,nth_cols):
		if self.isList==False:
			self.listInput()

		for line in self.lines:
			print line.split(delim)[nth_cols]

if __name__=="__main__":

	axl=AnaXSCALELP(sys.argv[1])
	llll=axl.getDataname('/',3)
	
