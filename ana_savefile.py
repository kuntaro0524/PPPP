import time
import datetime
import os
import sys
import pylab

class JobBlock:
	def __init__(self,blocklines):
		self.lines=blocklines
		self.isInit=False
		self.cnt_clean=0
		self.cnt_retry=0
		self.thead_00=0
		self.lhead_00=0
		self.thead_01=0
		self.lhead_01=0
		self.thead_02=0
		self.lhead_02=0

	def dispAll(self):
		print "#####################\n"
		print self.jobtype,self.status
		for line in self.lines:
			print "%s\n"%line,
		print "#####################\n"

	def getBlock(self):
		return self.lines

	def getStartTime(self):
		return self.start

	def isFailed(self):
		if self.status==0:
			return True
		else :
			return False

	def isCleaning(self):
		if self.cnt_clean==0:
			return False
		else:
			return True

	def storeInfo(self):
		# Start & End time
		self.calcTime()
		# Check job status
		self.checkJobStatus()
		# Count cleaning in this job
		self.countCleaning()
		# Count retry sequence
		self.countRetry()
		# Check 00
		self.getCheck00()
		self.getCheck01()
		self.getCheck02()
		# Check if the emergency button was pushed
		if self.status==0:
			self.checkEmButton()

	def checkEmButton(self):
		for line in self.lines:
			if line.find("An emergency stop")!=-1:
				self.status=4
				break
	def getInfo(self):
		str="%s %d %s %5d %5d %5d %5s %5s " % \
		(self.jobtypestr,self.status,self.start,self.total_time,self.cnt_clean,self.cnt_retry,self.thead_00,self.lhead_00)
	
		if self.thead_01!=0 and self.thead_02!=0:
			str2="%5s %5s %5s %5s\n"%(self.thead_01,self.lhead_01,self.thead_02,self.lhead_02)
		elif self.thead_01!=0:
			str2="%5s %5s\n"%(self.thead_01,self.lhead_01,self.thead_02,self.lhead_02)
		else:
			str2="\n"
		
		return str+str2

	def countRetry(self):
		for line in self.lines:
			if line.find("Retry")!=-1:
				self.cnt_retry+=1
			if line.find("Retray")!=-1:
				self.cnt_retry+=1

	def countCleaning(self):
		for line in self.lines:
			if line.find("Cleaning")!=-1:
				self.cnt_clean+=1

	def getCheck00(self):
		flag=0
		for line in self.lines:
			if line.find("Check 00")!=-1:
				flag=1
				continue
			if flag==1:
				iii=line.find("=")+1
				str1=line[iii:]
				str=str1.replace(", Lhead Spring =","")
				self.thead_00,self.lhead_00=str.split()
				break
	def getCheck01(self):
		flag=0
		for line in self.lines:
			if line.find("Check 01")!=-1:
				flag=1
				continue
			if flag==1:
				iii=line.find("=")+1
				str1=line[iii:]
				str=str1.replace(", Lhead Spring =","")
				self.thead_01,self.lhead_01=str.split()
				break

	def getCheck02(self):
		flag=0
		for line in self.lines:
			if line.find("Check 02")!=-1:
				flag=1
				continue
			if flag==1:
				iii=line.find("=")+1
				str1=line[iii:]
				str=str1.replace(", Lhead Spring =","")
				self.thead_02,self.lhead_02=str.split()
				break

	def checkJobStatus(self):
		# job type
		firstline=self.lines[0]

		# JOB type list
		# mount		: 0
		# unmount	: 1
		# cleaning	: 2
		# tray out	: 3

		if firstline.find("unmount")!=-1:
			self.jobtype=1
			self.jobtypestr="UNMOU"

		elif firstline.find("mount")!=-1:
			self.jobtype=0
			self.jobtypestr="MOUNT"

		elif firstline.find("cleaning")!=-1:
			self.jobtypestr="CLEAN"
			self.jobtype=2

		elif firstline.find("trayout")!=-1:
			self.jobtypestr="TRAYO"
			self.jobtype=3

		lastline=self.lines[len(self.lines)-1]

		# check job status
		# JOB status
		# failed	: 0
		# success	: 1
		# trayin	: 2
		if lastline.find("finished")!=-1:
			self.status=1
		elif lastline.find("Accident")!=-1:
			self.status=0
		else :
			self.status=2

	def calcTime(self):
		#print self.lines[0]
		self.start=self.getTime(self.lines[0])
		self.end=self.getTime(self.lines[len(self.lines)-1])
		self.total_time=(self.end-self.start).seconds

        def getTime(self,line):
                #print line[:12]
                # date
                ddd=int(line[:3])
                # hour
                hhh=int(line[3:5])
             	# min
		mmm=int(line[6:8])
                # sec
                sss=int(line[9:11])
                rt=datetime.datetime(2010,7,ddd,hhh,mmm,sss)
                return rt

class SPACElog:

	def __init__(self,filename):
		self.filename=filename
		self.isStored=False
		self.jblock=[]

	def storeLines(self):
		inf=open(self.filename)
		self.lines=inf.readlines()

		ppp=[]
		for line in self.lines:
			line=line.strip()
			ppp.append(line)

		self.lines=ppp
		self.isStored=True

	def dispAll(self):
		for block in self.jblock:
			block.dispAll()

	def storeJobBlock(self):
		if self.isStored!=True:
			self.storeLines()
		storeFlag=0 # mount: 1, umount: 2, cleaning: 3, tray in: 4

		tmplines=[]
		for line in self.lines:
			if line.find("I/put/bl_32in_sc_all/mount_")!=-1:
				tmplines.append(line)
				#print "FIND"
				storeFlag=1

			elif line.find("I/put/bl_32in_sc_all/unmount_")!=-1:
				tmplines.append(line)
				#print "FIND"
				storeFlag=2

			elif line.find("I/put/bl_32in_sc_all/cleaning")!=-1:
				tmplines.append(line)
				#print "FIND"
				storeFlag=3

			elif line.find("I/put/sc_all/trayout")!=-1:
				tmplines.append(line)
				storeFlag=4

			elif storeFlag==4 and line.find("I/put/sc_all/trayin")!=-1:
				tmplines.append(line)
				tmpblk=JobBlock(tmplines)
				self.jblock.append(tmpblk)
				tmplines=[]
				storeFlag=0

			elif storeFlag==3 and (line.find("Cleaning finished")!=-1 or line.find("Accident")!=-1):
				tmplines.append(line)
				#print "BREAK"
				tmpblk=JobBlock(tmplines)
				self.jblock.append(tmpblk)
				tmplines=[]
				storeFlag=0

			elif storeFlag==2 and (line.find("Unmount finished")!=-1 or line.find("Accident")!=-1):
				tmplines.append(line)
				#print "BREAK"
				tmpblk=JobBlock(tmplines)
				self.jblock.append(tmpblk)
				tmplines=[]
				storeFlag=0

			elif storeFlag==1 and (line.find("Mount finished")!=-1 or line.find("Accident")!=-1):
				#print "BREAK"
				tmplines.append(line)

				# initialize class
				tmpblk=JobBlock(tmplines)
				self.jblock.append(tmpblk)

				tmplines=[]
				storeFlag=0

			elif storeFlag!=0:
				tmplines.append(line)

	def makeTable(self,tblfile):
		self.storeJobBlock()

		ofile=open(tblfile,"w")

		idx=0
		for job in self.jblock:
			# prep data
			job.storeInfo()

			print "JOB.STOREINFO finished"

			# Failed job
			if job.isFailed():
				# Searching last cleaning
				sidx=idx
				while(1):
					print sidx
					sidx=sidx-1
					if sidx<0:
						break
					else:
						j=self.jblock[sidx]
						if j.isCleaning():
							self.last_clean=j.getStartTime()
							break
					
				ofile.write(job.getInfo())
				ofile.write("%s\n\n"%self.last_clean)
				#job.dispAll()
			idx+=1
		ofile.close()
		#self.makePlot(tblfile)

	def makePlot(self,tblfile):
		for job in self.jblock:
			job.storeInfo()

		pylab.plot(x,y)
		pylab.show()

if __name__=="__main__":

	slog=SPACElog(sys.argv[1])
	#slog.storeFailedLog()
	#slog.countTime()
	#slog.storeJobBlock()
	#slog.dispAll()

	logfile=sys.argv[1].replace(".txt","_ana.dat")
	slog.makeTable(logfile)
