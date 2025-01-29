import math
import os

class AnalyzeFWHM:
	def __init__(self,vx,vy):
		self.vx=vx
		self.vy=vy
		self.xsize=len(vx)
		self.ysize=len(vy)

		#print self.xsize,self.ysize
		if self.xsize!=self.ysize:
			print "Something wrong"
			os.exit()
	
	def calcDerivative(self):
		self.dx=[]
		self.dy=[]

		for cols in range(0,self.xsize-1):
			#print self.vy[cols],self.vy[cols+1]
			self.dx.append((self.vx[cols]+self.vx[cols+1])/2.0)
			self.dy.append(self.vy[cols]-self.vy[cols+1])

		self.len_der=len(self.dy)

		return self.dx,self.dy

	def calcDerivative2(self):
		#self.calcDerivative()
		self.dy2=[]

		for cols in range(0,self.len_der-1):
			self.dy2.append(self.dy[cols]-self.dy[cols+1])

		return self.dy2

class KnifeEdge:
	def __init__(self,rawfile):
		self.filename=rawfile
		self.prefix=rawfile.replace(".scn","")
		self.outfile=self.prefix+"_drv.scn"


	def writeDrvFile(self,n_derivative):
		ofile=open(self.outfile,"w")
		self.n_der=n_derivative

	## read file
		fin=open(self.filename,"r")
		lines=fin.readlines()
		self.x=[]
		self.y=[]
		self.dx=[]
		self.dy=[]
		self.dx2=[]
		self.dy2=[]
	##
		for line in lines:
			cols=line.split()
			self.x.append(float(cols[1]))
			self.y.append(float(cols[2]))

		self.af=AnalyzeFWHM(self.x,self.y)
		(dx,dy)=self.af.calcDerivative()

		self.af2=AnalyzeFWHM(dx,dy)
		(dx2,dy2)=self.af2.calcDerivative()

	# Derivetive1?
		if self.n_der==1:
			for i in range(0,len(dx)):
				line="12345 %12.3f %12.3f 12345\n" %(dx[i],dy[i])
				ofile.write(line)
	# Derivetive2?
		else:
			for i in range(0,len(dx2)):
				line="12345 %12.3f %12.3f 12345\n" %(dx2[i],dy2[i])
				ofile.write(line)

		fin.close()
		ofile.close()
		return self.outfile

if __name__=="__main__":

	test=KnifeEdge("00_dtheta1.scn")
	test.writeDrvFile(2)

