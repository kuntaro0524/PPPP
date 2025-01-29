import os,sys,math,numpy

class XDSrefl:
	def __init__(self,reffile):
		self.reffile=reffile

	def countRefl(self):
		ncount=0
		lines=open(self.reffile,"r").readlines()
		for line in lines:
			if line.rfind("!")!=-1:
				continue
			else:
				ncount+=1
		return ncount
