import math,os,sys
import scipy,time
import glob
from numpy import *
from Schedule_HSS_Re import *

class MakeSchedule:
	def __init__(self,schefile,datadir):
		self.schefile=schefile
		self.dd=datadir
		self.stepphi=0.1 # [deg.] rotation step
		self.steptrans=30.0 # [um] distance between irradiation points
		self.cl=140.0 # [mm] Camera length
		self.wl=1.2402 # [Angstrom] Wavelength
		self.prefix="data"
		self.margin=15.0 #[um]

	# Printing vector
	def printVec(self,vec,comment):
		print "%s: %12.5f %12.5f %12.5f"%(comment,vec[0],vec[1],vec[2])

	def setStepPhi(self,stepphi):
		self.stepphi=stepphi

	def setCL(self,cl):
		self.CL=cl

	def setWL(self,wl):
		self.wl=wl

	def setPrefix(self,prefix):
		self.prefix=prefix

	# This return
	# 0: Failed (No schedule files are generated
	# 1: OK (some schedule files are generated
	def makeMergedSchedule(self):

		# Check how many schedule files were generated?
		schlist=glob.glob("/tmp/*.sch")
		if len(schlist)==0:
			print "No schedule files!"
		
		else:
		# Merge all of /tmp/tmp_*.sch
			command="cat /tmp/*.sch > %s" % self.schefile
			os.system(command)
			return 1

	def readGonioFile(self,filename):
		lines=open(filename).readlines()
		vec_list=[]
		for line in lines:
			cols=line.split()
			x,y,z=float(cols[0]),float(cols[1]),float(cols[2])
			vec_list.append([x,y,z])
		return vec_list

	# vec_list: includes A,B,C,D Gonio coordinates
	def setVectors(self,vec_list):
	#########################################################
	# Gonio coordinates
	#########################################################
		self.g01=vec_list[0]
		self.g02=vec_list[1]
		self.g03=vec_list[2]
		self.g04=vec_list[3]

	#####################################################
	# vector calculation
	# All of crystal-shape-vectors are checked if 
	# they have cross points with Y-vector 
	#####################################################
	def getCrossPoint(self,vec1,vec2,yl):
		# vec1 : start
		# vec2 : end 
		# yl : y coordinate of tatesen
		# EX) vec(P)=vec(A)+a*vec(AD)
	
		# Line vector of vec1-vec2
		line_vec=vec2-vec1
	
		a=(yl-vec1[1])/line_vec[1]
		#print "partial:",a
	
		if a <0.0 or a>1.0:
			return array([0,0,0])
		else:
			vecp=vec1+a*line_vec
			return vecp

	def generateSchedule(self,shoumenphi,inc_angle):
		print "INC_ANGLE=",inc_angle
		#####################################################
		# Initial definitions PHI
		#####################################################
		#shoumenphi=float(sys.argv[2]) # This is shoumen
		#startphi=float(sys.argv[3])   # This is start angle for this crystal
		stepphi=self.stepphi

		#####################################################
		# Step length
		#####################################################
		step=self.steptrans # [um] distance between irradiation points
		
		#####################################################
		# Sort by Y coordinates
		# Point vector [um]
		#####################################################
		A=array(self.g01)*1000.0
		B=array(self.g02)*1000.0
		C=array(self.g03)*1000.0
		D=array(self.g04)*1000.0

		self.printVec(A,"A:")
		self.printVec(B,"B:")
		self.printVec(C,"C:")
		self.printVec(D,"D:")

		#####################################################
		# Y coordinate min&max
		#####################################################
		maxy=A[1]
		miny=C[1]
		print "Max & Min Y coordinates",maxy,miny

		#####################################################
		# Y length of this crystal
		#####################################################
		len_y=int(math.floor(maxy-miny))
		print "marumeta size(Y):",len_y

		# Number of Y lines for this crystal
		shou,amari=divmod(len_y,step)
		print "SHOU/AMARI=",shou,amari
		
		if amari!=0:
			ny=int(shou)
		else:
			ny=int(shou)-1

		print "number of Y lines=",ny

		#####################################################
		# Each Y coordinate
		#####################################################
		start_y=maxy # Left point

		# Turning points
		ya=A[1]
		yb=B[1]
		yc=C[1]
		yd=D[1]
		
		#####################################################
		# Crosspoint wo shiraberu houhou
		# Shiraberu vectors : AB, BC, CD, DA
		# They are crystal-shape-vectors
		#####################################################
		svec_evecs=[]
		for i in arange(0,ny,1):
			yp=start_y-float(i+1)*step
			#print "Y code:",yp
			# Y baaiwake
			# AB vector
			#print "Vector AD and AB"
			P=self.getCrossPoint(A,B,yp)
			Q=self.getCrossPoint(B,C,yp)
			R=self.getCrossPoint(C,D,yp)
			S=self.getCrossPoint(D,A,yp)
		
			targ=[]
			for U in (P,Q,R,S):
				if U[1]!=0.0:
					targ.append(U)
				else:
					continue
			svec_evecs.append(targ)

		# Each Yl line
		n_total=0
		n_vecs=0
		ofile=open("p.txt","w")
		
		n_crystal=0
		n_points=0
		TotalTime=0.0
		
		# remove all of /tmp/tmp_*.sch
		command="rm -f /tmp/*.sch"
		os.system(command)
		
		# Start serial number of this crystal
		serial_offset=int((inc_angle+60.0)/stepphi)
		
		# pair vector having same Yl coordinate
		for svec_evec in svec_evecs:
			# number of vectors in this crystal
			n_vecs+=1
			# Start PHI: inclination from shoumen : phi0
			inc_angle0=inc_angle+float(n_total)*stepphi
		
			## Simply from cross point calculation
			# Start vector (XYZ)
			svec=svec_evec[0]
			# End vector (XYZ)
			evec=svec_evec[1]
		
			# Start -> End vector
			sevec=evec-svec
		
			# Length of the initial vector (Absolute length)
			L=linalg.norm(sevec)
			print "LOG: Absolute length of the start-end vector: %8.1f [um]"%L
		
			# Base translation vector of START->END vector (1um length)
			# this is used for making irradiation point vectors
			tunit=sevec/linalg.norm(sevec)
		
			# PHI on Hardware
			phi_hw=shoumenphi+inc_angle0
			print phi_hw
		
			# Margine length viewed from X-ray
			marginX=self.margin/cos(radians(inc_angle0))

			# CASE: Margine is longer than the original vector
			if marginX > L:
				print "Margine is very big"
				continue
		
			# Margins-added START & END vectors
			# Start vector
			startvec=svec+marginX*tunit
			endvec=evec-marginX*tunit
		
			# New start & end vectors
			nsevec=endvec-startvec
		
			# Absolute length of the new start-end vector
			L_new=linalg.norm(nsevec)
			print "LOG: Absolute length of the vector without margin:          %8.1f [um]"%L_new
		
			# Length of this vector from X-ray view-point
			lse=L_new*cos(radians(inc_angle0))
			print "LOG: Absolute length of the irradiation vector(from X-ray): %8.1f [um]"%lse
		
			######################################
			# Vector is unused when
			# margin x 2 < length of final vector viewed from X-ray
			######################################
			if lse < 2.0*self.margin:
				print "This vector cannot be used because the length is too short."
				continue
		
			# possible number of irradiation points on the 'nsevec'
			tmp_lse=int(math.floor(lse))
			tmp_step=int(math.floor(step))
			shou,amari=divmod(tmp_lse,tmp_step)
			np=shou+1
		
			print "LOG: Number of irradiation points:",np
		
			# Exists?
			if np > 0:
				n_total+=np
				n_points+=np # irradiation points of this crystal
			else: 
				continue
		
			# Movement vector
			mvec=(step/cos(radians(inc_angle0)))*tunit
		
			# Making schedule files
			# N th vectors in this crystal
			schedule_file="/tmp/tmp_%03d.sch"%n_vecs
			print "SCHEDULE_FILE: %s"%schedule_file
		
			#################################
			# Start PHI and End PHI
			#################################
			phi_start00=phi_hw
			phi_end00=phi_start00+float(np)*stepphi

			print "Scan phi-end",phi_start00,phi_end00
		
			################################
			# Vectors
			# Length of movement vector
			# this is same with linalg.norm(mvec)
			################################
			astep=linalg.norm(mvec) #[um]
			ssvec=startvec/1000.0 # [mm]
			eevec=endvec/1000.0 # [mm]
		
			################################
			# Setting parameters to 
			################################
			# Static parameters
			#class Schedule_HS_Re:
			t=Schedule_HS_Re()
			t.setDir(self.dd)
			t.setWL(self.wl)
			t.setDataName(self.prefix)
			t.setCameraLength(self.cl)
			t.setOffset(serial_offset)
			t.setExpTime(1.0)
			t.sfrox(ssvec,eevec,phi_start00,stepphi,np,astep)
			t.setAttIdx(0)
			t.setScanInt(1)
			t.make(schedule_file)
		
			#################################
			# Serial offset
			# Shoumen = 0.0 deg
			# Startphi = -60.0 deg
			################################
			print "START SERIAL of this vector",serial_offset
			serial_offset+=np
			end_offset=serial_offset-1
			print "END   SERIAL of this vector",end_offset
		
			print "Total points:",n_total
		
		# This crystal : points
		print "N points/crystal=",n_points
		collection_time=n_points*5.0/60.0 #[min]
		centering_time=10 #[min]
		time_cycle=collection_time+centering_time
		print "Time for this crystal=",time_cycle,"[min]"
		TotalTime+=time_cycle
			
		print "1TIME:",TotalTime/60.0, " 2TIME:",TotalTime/30.0
		return n_total
		
if __name__ == "__main__":
	ms=MakeSchedule("./sch.sch","/isilon/users/taret/target/Staff/2014B/test")
	vec_list=ms.readGonioFile(sys.argv[1])
	ms.setPrefix("cco_demo")
	ms.setVectors(vec_list)
	ms.generateSchedule(0.0,0.0)
	ms.makeMergedSchedule()
