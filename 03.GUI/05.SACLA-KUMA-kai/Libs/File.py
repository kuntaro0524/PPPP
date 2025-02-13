import sys
import os
import glob
import datetime
from stat import *
from Date import *

class File:
	def __init__(self,directory):
		self.dire=directory

	def listSuffix(self,suffix):
		#print "%s/*%s"%(self.dire,suffix)
		file="%s/*%s"%(self.dire,suffix)
		self.list=glob.glob(file)
		self.list.sort()
		return self.list

	def getHomeDire(self):
		return os.environ['HOME']

	def checkWritePermission(self,path):
		return os.access(path, os.W_OK)

	def isExistDire(self,path):
		return os.access(path, os.F_OK)

	def getTargetStaff(self):
		#dire="/isilon/BL32XU/BL/target/Staff/"
		dire="/isilon/BL32XU/BLtune/"
		return dire

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
		return os.path.abspath(self.dire)

	def changeSuffix(self,filename,newsuffix):
		last_idx_dot=filename.rfind(".")
		prefix=filename[:last_idx_dot]
		newfile=prefix+"."+newsuffix

		return(newfile)

	def stripPath(self,filename):
		last_idx_slash=filename.rfind("/")
		prefix=filename[last_idx_slash+1:]
		return prefix

	def timeDire(self):
		d=Date()
		tdy_dir=d.getTodayDire()
		time_dir=d.getTimeDire()

		rtnstr="%s/%s"%(tdy_dir,time_dir)
		return rtnstr

	def makeTimeDires(self):
		# Staff directory
		dir="%s/%s"%(self.getTargetStaff(),self.timeDire())
		# check if the 'path' exists
		if self.isExistDire(dir):
			return dir
		else:
			os.makedirs(dir)
			return dir

	def getTime(self,filename):
		d=Date()
		#print filename
		timeget=os.stat(filename)[ST_MTIME]
		output_fmt="%Y/%m/%d %H:%M:%S"
		time_fmt=time.strftime(output_fmt,time.localtime(timeget))

		t=d.getOkutsuTime(time_fmt)
		return t

	def getDiffTime(self,file1,file2):
		d=Date()
		d1=self.getTime(file1)
		d2=self.getTime(file2)
		#print d1,d2
		secs=d.getDiffSec(d1,d2)
		return secs

	def getPrefixList(self,prefix):
		listname="%s/%s*"%(self.dire,prefix)
		#print listname
                flist=glob.glob(listname)
		return flist

	def getPrefixSuffixList(self,prefix,suffix):
		listname="%s*%s"%(prefix,suffix)
		#print listname
                flist=glob.glob(listname)
		return flist
		
if __name__=="__main__":

	f=File("./")
	#i2= f.getNewIdx2()
	#i3= f.getNewIdx3()

	#print i2,i3

	print "%03d"%(f.getNewIdx3())

	#print f.getCurrentPath()
	#print f.timeDire()
	#dir="%s/%s"%(f.getTargetStaff(),f.timeDire())
	#print dir
	#print f.isExistDire(dir)
	#f.makeTimeDires()
	#print f.getTime(sys.argv[1])
	#print f.getDiffTime(sys.argv[1],sys.argv[2])
	#print f.getPrefixList(sys.argv[1])
	#print f.isExistDire(dir)
	#print f.checkWritePermission(dir)
