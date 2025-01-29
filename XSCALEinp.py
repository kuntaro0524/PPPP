import sys,os,math


class XSCALEinp:
	def __init__(self,inpfile):
		self.inpfile=inpfile
		self.isInit=False

	def init(self):
		self.lines=open(self.inpfile).readlines()
		self.isInit=True

	def getInputList(self):
		if self.isInit==False:
			self.init()

		self.input_files=[]
		for line in self.lines:
			line=line.strip()
			if line.rfind("INPUT_FILE=")!=-1:
				store_str=line.replace("INPUT_FILE=","").replace(" ","").replace("*","")
				self.input_files.append(store_str)
		return self.input_files	

if __name__=="__main__":
	xsi=XSCALEinp("XSCALE.INP")
	print xsi.getInputList()
