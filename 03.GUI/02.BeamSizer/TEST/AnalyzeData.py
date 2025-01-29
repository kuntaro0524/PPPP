import math
import os
import sys
class AnalyzeData:

	def __init__(self,datfile,option):
		self.fname=datfile
		self.isRead=0
		self.option=option

	def __readColumn(self):
		self.cols=[]
		# count a number of columns
		f=open(self.fname,"r")
		lines=f.readlines()
		f.close()

		for line in lines:
			if line.strip().find("#")==0:
				continue

			new=[]
			new=line.strip().split()

			self.cols.append(line.strip().split())

		#print self.cols
		self.ncols=len(self.cols)

	def storeData(self,col_x,col_y):
		self.__readColumn()
		self.xdat=[]
		self.ydat=[]

		for idx in range(0,self.ncols):
			self.xdat.append(float(self.cols[idx][col_x]))
			self.ydat.append(float(self.cols[idx][col_y]))

	def calcDrv(self):
		dx,dy=self.derivative(self.xdat,self.ydat)
		return self.dx,self.dy

	def scaleY(self,scale):
		self.yscale=[]

		print "scale factor %8.5f"%scale

		for idx in range(0,self.ncols):
			self.yscale.append(self.ydat[idx]*scale)

	def writeScaled(self,ofile):
		of=open(ofile,"w")
		ndata=len(self.xdat)

		for i in range(0,ndata):
			of.write("12345 %12.5f %12.5f %12.5f\n"%(self.xdat[i],self.yscale[i],self.ydat[i]))

		of.close()

	def writePeak(self,ofile):
		of=open(ofile,"w")
		ndata=len(self.xdat)
		#print ndata

		for i in range(0,ndata):
			#print i
			of.write("12345 %12.5f %12.5f 12345\n"%(self.xdat[i],self.ydat[i]))

		of.close()

	def writeDrv(self,ofile):
		of=open(ofile,"w")
		ndata=len(self.dx)
		#print ndata

		for i in range(0,ndata):
			#print i
			of.write("12345 %12.5f %12.5f 12345\n"%(self.dx[i],self.dy[i]))

		of.close()

	def normalizePeak(self,col_x,col_y,ofile):
		of=open(ofile,"w")

		if self.isRead==0:
			self.__readColumn()
		self.storeData(col_x,col_y)
		self.findHalf(self.xdat,self.ydat)

		ndata=len(self.xdat)

		for i in range(0,ndata):
			self.ydat[i]=float(self.ydat[i])/float(self.maxvalue)

		self.writePeak(ofile)

	def findHalf(self,xarray,yarray):
		self.maxx=0
		self.maxvalue=-9999.9999
		# max & min derivativs
		for idx in range(0,len(xarray)):
			if self.maxvalue<yarray[idx]:
				self.peakx=idx
				self.maxx=xarray[idx]
				self.maxvalue=yarray[idx]

		#print self.maxx,self.maxvalue
		self.halfvalue=self.maxvalue/2.0

	def getDerivative(self):
		return self.dx,self.dy

	def getData(self):
		return self.xdat,self.ydat

	def normalize(self,col_x,col_y,ofile):
		if self.option=="peak":
			self.normalizePeak(col_x,col_y,ofile)

	def analyze(self,col_x,col_y):
		if self.option=="peak":
			fwhm,fcen=self.analyzePeak(col_x,col_y)
		elif self.option=="knife":
			fwhm,fcen=self.analyzeKnife(col_x,col_y)

		return fwhm,fcen

	def drvCenter(self,col_x,col_y):
		if self.isRead==0:
			self.__readColumn()
			self.storeData(col_x,col_y)
		self.calcDrv()
		mini,maxi=self.findMinMax(self.dy)
		drvcenter=(self.dx[mini]+self.dx[maxi])/2.0
		#self.writeDrv("ping.dat")
		return drvcenter

	def analyzeKnife(self,col_x,col_y):
		if self.isRead==0:
			self.__readColumn()
		self.storeData(col_x,col_y)
		self.calcDrv()
		self.findHalf(self.dx,self.dy)
		t,y=self.calcFWHM(self.dx,self.dy)
		return t,y

	def analyzePeak(self,col_x,col_y):
		if self.isRead==0:
			self.__readColumn()
		self.storeData(col_x,col_y)
		self.findHalf(self.xdat,self.ydat)
		t,y=self.calcFWHM(self.xdat,self.ydat)
		return t,y

	def calcFWHM(self,xarray,yarray):
		peak_flag=0

		# Initialization
		self.smallx=-999.999
		self.largex=-999.999

		# print
		#for i in range(0,len(xarray)-1):
			#print xarray[i],yarray[i]

		# before peak
		for idx in range(0,len(xarray)-1):
			#print idx
			#print yarray[idx],yarray[idx+1],self.halfvalue
			if yarray[idx] <= self.halfvalue and yarray[idx+1] >= self.halfvalue:
				grad1=(yarray[idx+1]-yarray[idx])/(xarray[idx+1]-xarray[idx])
				sepp1=yarray[idx]-grad1*xarray[idx]
				
				#print "Y=%5.3f x + %5.3f" % (grad1,sepp1)
				self.smallx=(self.halfvalue-sepp1)/grad1
				break

		for idx in range(0,len(xarray)-1):
			if yarray[idx] >= self.halfvalue and yarray[idx+1] <= self.halfvalue:
				grad2=(yarray[idx+1]-yarray[idx])/(xarray[idx+1]-xarray[idx])
				sepp2=yarray[idx]-grad2*xarray[idx]
				
				#print "Y=%5.3f x + %5.3f" % (grad2,sepp2)
				self.largex=(self.halfvalue-sepp2)/grad2
				break

		if self.smallx==-999.999 or self.largex==-999.999:
			print "FWHM cannot be calculated!"
			return -999.999

		# FWHM center
		if grad1!=grad2:
			fcen=-(sepp1-sepp2)/(grad1-grad2)
		else:	
			print "FWHM calculation failed"

		fwhm=math.fabs(self.smallx-self.largex)
		#print "FWHM=%8.4f"%(math.fabs(self.smallx-self.largex))
		#print "FWHM center=%8.4f"% fcen

		return  fwhm,fcen

	def calcDrv2(self,col_x,col_y):

		self.ddx=[]
		self.ddy=[]

		if len(self.dx)==0:
			self.dx,self.dy=self.calcDrv(col_x,col_y)

		self.ddx,self.ddy=self.derivative(self.dx,self.dy)

		for idx in range(0,len(self.dx)):
			print "%12.5f %12.5f" %(self.dx[idx], self.dy[idx])


        def derivative(self,xdat,ydat):
                self.dx=[]
                self.dy=[]

		self.xsize=len(self.xdat)
		self.ysize=len(self.ydat)

		if self.xsize==0 or self.ysize==0:
			print "Size of arrays is 0"
			return 0

                for cols in range(0,self.xsize-1):
                        self.dx.append((xdat[cols]+xdat[cols+1])/2.0)
                        self.dy.append(ydat[cols]-ydat[cols+1])

		return self.dx,self.dy

	def findPeak(self,col,type):
		if self.isRead==0:
			self.__readColumn()

		#print self.ncols
		
		maxvalue=-999999.99999

		for idx in range(0,self.ncols):
			tmp=float(self.cols[idx][col])
			if tmp > maxvalue:
				maxvalue=tmp

		if type=="int":
			return int(maxvalue)
		elif type=="float":
			return float(maxvalue)
		elif type=="char":
			return str(maxvalue)

	def findMinMax(self,data_array):
		ndata=len(data_array)
		maxvalue=-999999999.99999
		minvalue=99999999.99999

		min_index=0
		max_index=0

		if ndata==0:
			print "Array is not good"
			return -1
		for i in range(0,ndata):
			if(maxvalue < data_array[i]):
				maxvalue=data_array[i]
				max_index=i
			if(minvalue > data_array[i]):
				minvalue=data_array[i]
				min_index=i
			else :
				continue

		return min_index,max_index

if __name__=="__main__":
	        #test=AnalyzeData(sys.argv[1],"peak")
		#test.test(1,2)
		#fwhm,center=test.analyze(1,2)
		#print "FWHM=%8.4f"% fwhm
		#print "FWHM center=%8.4f"% center
		##test.printDrv()

		test=AnalyzeData(sys.argv[1],"peak")
		#test.storeData(1,3)
		#test.scaleY(float(sys.argv[2]))
		#test.writeScaled("scaled.dat")

		test.normalize(1,2,"norm.dat")

