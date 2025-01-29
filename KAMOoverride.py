import sys,math,os
import DirectoryProc

class KAMOoverride():
	def __init__(self,target_dire):
		self.target_dire=target_dire
		self.direproc=DirectoryProc.DirectoryProc(target_dire)
		self.dires=self.direproc.getDirList()

	def setDirectory(self,include_string):
		new_list=[]
		for dire in self.dires:
			print dire
			if dire.rfind(include_string)!=-1:
				new_list.append(dire)
				print dire
		print self.dires
		self.dires=new_list
		print self.dires

	def beamOverride(self,orgx,orgy):
        	for dire in self.dires:
			print dire
			oname="%s/data/kamo_override.config"%dire
			ofile=open(oname,"w")
			ofile.write("orgx= %4d\n"%orgx)
			ofile.write("orgy= %4d\n"%orgy)

if __name__=="__main__":

	ko=KAMOoverride(sys.argv[1])
	ko.setDirectory(sys.argv[2])
	ko.beamOverride(1552.1,1591.97)
