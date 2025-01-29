import sys
import os
import glob

class File:
	def __init__(self,directory):
		self.dire=directory

	def listScn(self):	
		file="%s/*img"%self.dire

		self.list=glob.glob(file)
		return self.list

	def getAbsolutePath(self):
		return os.path.abspath(self.dire)

	def getCurrentPath(self):
		return os.path.abspath(self.directory)

if __name__=="__main__":

	f=File("../")
	
	for file in f.listScn():
		#print file
		origfile=file.replace("\\","\\\\")
		newfile=file.replace("\\","-")
		#print origfile 
		#print newfile
		print "mv %s %s"%(origfile,newfile)
		#print file.find("\\")
		#print f.getAbsolutePath(file)

	#print f.getAbsoluteDir("./")
