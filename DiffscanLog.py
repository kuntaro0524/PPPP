import os
import sys
import math
#from  pylab import *
import socket
import pylab
import scipy
import numpy
#from numpy import *
from pylab import *
from MyException import *

class DiffscanLog:

	def __init__(self,logfile):
		self.filename=logfile
		self.lines=[]
		self.nscan=0
		self.allblocks=[] 	# strings of XYZ information
		self.allxyz=[]		# list of (scanID,pointindex,x,y,z)
		self.allstep=[]		# list of (Nv,Nh,step(v),step(h))
		self.isInit=False

	########################################3
	# this routine should be called whenever a log is read
	# process
	# 1. read lines
	# 2. count scan jobs
	# 3. make a list of jobs
	########################################3
	def prep(self):
        	self.readfile()
        	self.countScan()
        	self.storeList()
		self.isInit=True
		self.storeDimension()
		return self.nscan

	#)
	#) A simple function to read lines
	#)
	def readfile(self):
		ifile=open(self.filename,"r")
		self.lines=ifile.readlines()
		ifile.close()

	# --------
	#) This class function 
	#) 1) compiles each diffraction scan information 
	#)    to a list of a list of strings
	#  --> Brief description
	#  a list "blockline[]" includes lines of each scan
	#  a class variant "self.allblocks[]" include "blockline"
	#
	#  2) Count a number of all jobs
	#  3) make a list of 
	# =======
	# Data access
	# =======
	# self.allblocks[0] -> a list of string lines of the '1st' scan
	# --------
	def countScan(self):
		blockline=[]
		readflag=False

		for line in self.lines:
			if line.find("Diffraction scan")!=-1:
				readflag=True
			# count scan
				self.nscan+=1
				#print "TRUE"
				continue

			if readflag==True and line.find("======")!=-1:
				readflag=False
				#blockline.append(line)
				self.allblocks.append(blockline)
				blockline=[]
				
			if readflag==True:
				blockline.append(line)

		### Acquire nscan
		#print "Current scan #:= %5d"%self.nscan

	#####
	# This class function 'storeList'
	# 1) extracts gonio XYZ information from stored 'string' information 'allblocks'
	# 2) stored float values into the class variant 'allxyz' 
	#    (Data structure) list of '[scan number],[scan index],[x],[y],[z]'
	#####
	def storeList(self):
		#print self.allblocks
		#print len(self.allblocks)
		code=[]
		for i in range(0,len(self.allblocks)):
			readflag=False
			#print "=====SCAN NO. %d ====="%i
			for line in self.allblocks[i]:
				if line.find("Camera")!=-1:
					readflag=True
					continue
				if readflag:
					cols=line.split()
					if len(cols)==4:
						idx=int(cols[0])
						cx=float(cols[1])
						cy=float(cols[2])
						cz=float(cols[3])
						ds=i,idx,cx,cy,cz
						code.append(ds)
			self.allxyz.append(code)
			code=[]

		#print "GETLIST"
		##print self.allxyz
		#print "GETLIST"

	def storeDimension(self):
		if self.isInit==False:
			self.prep()
		
		for i in range(0,len(self.allblocks)):
			readflag=False
			for line in self.allblocks[i]:
				if line.find("Vertical")!=-1:
					cols=line.split()
					nv= int(cols[5])
					sstep=cols[7][:len(cols[7])-2]
					vs= float(sstep)
					
				elif line.find("Horizontal")!=-1:
					cols=line.split()
					nh= int(cols[5])
					sstep=cols[7][:len(cols[7])-2]
					hs= float(sstep)
					break
			ll=nv,nh,vs,hs
			self.allstep.append(ll)

	# return the 'index'th block (IDX,X,Y,Z)
	def getBlock(self,index):
		tmpxyz=[]
		for block in self.allxyz:
			for xyz in block:
				if xyz[0]==index:
					si=int(xyz[0])
					ti=int(xyz[1])
					tx=float(xyz[2])
					ty=float(xyz[3])
					tz=float(xyz[4])
					list=si,ti,tx,ty,tz
					tmpxyz.append(list)
					#print "%5d %8.4f %8.4f %8.4f"%(ti,tx,ty,tz)
		return tmpxyz

	def getNewestScan(self):
		if self.isInit==False:
			self.prep()
		#print self.allblocks
		idx=self.nscan-1
		#print self.allstep[idx]
		#print self.allxyz[idx]
		return self.allstep[idx],self.getBlock(idx)

	def get2Didx(self,ipoint,nv,nh):
		v=ipoint/(nh+1)+1
		h=ipoint-((v-1)*nh)
		#print v,h
		return v,h

	def getCodeList(self,iscan):
		return(self.getBlock(iscan))

	def getPosition(self,iscan,ipoint):
		iscan=iscan-1
		ipoint=ipoint-1

		xyzlist=self.getBlock(iscan)

		x=y=z=0.0
		for i in range(0,len(xyzlist)):
			#if xyzlist[1]==ipoint:
			print xyzlist[1]
			if int(xyzlist[i][1])==ipoint:
				x= xyzlist[i][2]
				y= xyzlist[i][3]
				z= xyzlist[i][4]
				break

		return float(x),float(y),float(z)

	def getPrevious(self):
		idx=self.nscan-2
		if idx<0:
			print "You may not have a previous scan yet."
			return
		else:
			self.getBlock(idx)

if __name__=="__main__":
	dl=DiffscanLog("diffscan.log")
	dl.prep()
	p,q= dl.getNewestScan()

	xyzlist=dl.getCodeList(0)

	for xyz in xyzlist:
		print "%8.5f"%(xyz[3])

	#dl.storeDimension()
	#nv,nh,sv,sh=p
	#print nv,nh,sv,sh

	#n=nv*nh
	#for i in range(1,n+1):
		#print i
		#dl.get2Didx(i,nv,nh)
	#print dl.getPosition(3,5)

	#print "PREVIOUS"
	#dl.getPrevious()
