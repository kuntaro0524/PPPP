import sys
import os
import glob

class File:
	def __init__(self,directory):
		self.dire=directory

	def listSuffix(self,suffix):
		#print "%s/*%s"%(self.dire,suffix)
		file="%s/*%s"%(self.dire,suffix)
		self.list=glob.glob(file)
		return self.list

	def getHeadNum(self,name,nchar):
		if os.path.isfile(name)==False:
			return ("00")

		last_idx=name.rfind("/")
		simple_name=name[last_idx+1:]

		header=simple_name[:nchar]
		if header.isdigit():
			return(header)
		else:
			return("00")

	def getNewIdx(self,suffix):
		flist=self.listSuffix(suffix)

		max=0
		if len(flist)==0:
			return 0

		for file in flist:
			curr=self.getHeadNum(file)
			if max<curr:
				max=curr
		return int(max)+1

	def getNewIdx2(self):
		flist=glob.glob("*")

		max=0
		if len(flist)==0:
			return 0

		for file in flist:
			curr=self.getHeadNum(file,2)
			#print curr
			if max<curr:
				max=curr
		return int(max)+1

	def getNewIdx3(self):
		flist=glob.glob("*")

		max=0
		if len(flist)==0:
			return 0

		for file in flist:
			curr=self.getHeadNum(file,3)
			#print max,curr
			if max<curr:
				#print "FIND!!"+curr
				max=curr
		return int(max)+1

	def listScn(self):	
		file="%s/*py"%self.dire
		self.list=glob.glob(file)
		return self.list

	def getAbsolutePath(self):
		return os.path.abspath(self.dire)

	def getCurrentPath(self):
		return os.path.abspath(self.directory)

	def changeSuffix(self,filename,newsuffix):
		last_idx_dot=filename.rfind(".")
		prefix=filename[:last_idx_dot]
		newfile=prefix+"."+newsuffix

		return(newfile)

if __name__=="__main__":

	f=File("./")
	i2= f.getNewIdx2()
	i3= f.getNewIdx3()

	print i2,i3
	
	#newfile=f.changeSuffix("test.scn","png")

	#print newfile

	#for file in f.listSuffix("scn"):
		#print file
		#print f.getHeadNum(file)
		#origfile=file.replace("\\","\\\\")
		#newfile=file.replace("\\","-")
		#print origfile 
		#print newfile
		#print "mv %s %s"%(origfile,newfile)
		#print file.find("\\")
		#print f.getAbsolutePath(file)

	#print f.getAbsoluteDir("./")
