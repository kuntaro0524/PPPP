import sys,os,math
import glob

class ZOO_scan:

	def __init__(self,dcpath):
		self.dcpath=dcpath
		self.scanpath0=os.path.abspath(dcpath)+"/scan/"
		print self.scanpath0

	def getMaster(self):
		self.master_list=glob.glob("%s/*master*"%self.scanpath0)
		print self.master_list

if __name__=="__main__":
	zs=ZOO_scan("/isilon/users/target//target/AutoUsers/171002/hirota/hirota-HIR0001-01/")
	zs.getMaster()
