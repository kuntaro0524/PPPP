import math,os,sys
import scipy,time
from numpy import *
from Schedule_HSS_Re import *

# Printing vector
def printVec(vec,comment):
	print "%s: %12.5f %12.5f %12.5f"%(comment,vec[0],vec[1],vec[2])

def readGonioFile(filename):
	lines=open(filename).readlines()
	vec_list=[]
	for line in lines:
		cols=line.split()
		#print cols
		x,y,z=float(cols[0]),float(cols[1]),float(cols[2])
		vec_list.append([x,y,z])
	return vec_list

vec_list=readGonioFile(sys.argv[1])

#########################################################
# Gonio coordinates
#########################################################
g01=vec_list[0]
g02=vec_list[1]
g03=vec_list[2]
g04=vec_list[3]

#####################################################
# Initial conditions
#####################################################

if len(sys.argv)!=6:
	print "Usage: python this GONIOFILE FACEPHI STARTPHI STEPPHI STEPLENGTH[um]"
	sys.exit()

#####################################################
# Initial static settings for this crystal
#####################################################
# Data output directory
outdir="/isilon/users/target/target/Staff/2014B/150209/00.CcOTest/po1129_021/"
wavelength=1.0 # Angstrom
cameralength=150.0 #mm
prefix="cco_demo"

#####################################################
# Initial definitions PHI
#####################################################
shoumenphi=float(sys.argv[2]) # This is shoumen
startphi=float(sys.argv[3])   # This is start angle for this crystal
endphi=startphi+135.0 # This is the end rotation 
stepphi=float(sys.argv[4]) # interval angle for each irradiation point

#####################################################
# Step length
#####################################################
step=float(sys.argv[5]) #[um]

#####################################################
# Sort by Y coordinates
# Point vector [um]
#####################################################
A=array(g01)*1000.0
B=array(g02)*1000.0
C=array(g03)*1000.0
D=array(g04)*1000.0

printVec(A,"A")
printVec(B,"B")
printVec(C,"C")
printVec(D,"D")

#####################################################
# Y coordinate min&max
#####################################################
maxy=A[1]
miny=C[1]
print maxy,miny

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
#print miny,maxy

# Turning points
ya=A[1]
yb=B[1]
yc=C[1]
yd=D[1]

#####################################################
# vector calculation
# All of crystal-shape-vectors are checked if 
# they have cross points with Y-vector 
#####################################################
def getCrossPoint(vec1,vec2,yl):
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
	P=getCrossPoint(A,B,yp)
	Q=getCrossPoint(B,C,yp)
	R=getCrossPoint(C,D,yp)
	S=getCrossPoint(D,A,yp)

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

margin=15.0 #[um]

# remove all of /tmp/tmp_*.sch
command="rm -f /tmp/*.sch"
os.system(command)

# Start serial number of this crystal
inclination_from_m60deg=startphi-shoumenphi+60.0
serial_offset=int(inclination_from_m60deg/stepphi)

# pair vector having same Yl coordinate
for svec_evec in svec_evecs:
	# number of vectors in this crystal
	n_vecs+=1
	# Start PHI
	phi0=startphi+float(n_total)*stepphi
	print "LOG: StartPhi of this vector=%5.1f"%(phi0)

	## Simply from cross point calculation
	# Start vector (XYZ)
	svec=svec_evec[0]
	# End vector (XYZ)
	evec=svec_evec[1]

	# Start -> End vector
	sevec=evec-svec

	# Length of the initial vector (Absolute length)
	L=linalg.norm(sevec)
	print "LOG: Absolute length of the initial vector: %8.1f [um]"%L

	# Base translation vector of START->END vector (1um length)
	# this is used for making irradiation point vectors
	tunit=sevec/linalg.norm(sevec)

	# PHI value from shoumen
	phi_rel=phi0-shoumenphi

	# Margine length viewed from X-ray
	marginX=margin/cos(radians(phi_rel))

	# Margins-added START & END vectors
	# Start vector
	startvec=svec+marginX*tunit
	endvec=evec-marginX*tunit

	# New start & end vectors
	nsevec=endvec-startvec

	# Absolute length of the new start-end vector
	L_new=linalg.norm(nsevec)
	print "LOG: Absolute length of the NEW vector:           %8.1f [um]"%L_new

	# Length of this vector from X-ray view-point
	lse=L_new*cos(radians(phi_rel))
	print "LOG: Absolute length of the final vector(from X-ray): %8.1f [um]"%lse

	######################################
	# Vector is unused when
	# margin x 2 < length of final vector viewed from X-ray
	######################################
	if lse < 2.0*margin:
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
	mvec=(step/cos(radians(phi_rel)))*tunit

	# Making schedule files
	# N th vectors in this crystal
	schedule_file="/tmp/tmp_%03d.sch"%n_vecs
	print "SCHEDULE_FILE: %s"%schedule_file

	#################################
	# Start PHI and End PHI
	#################################
	phi_start00=phi0
	phi_end00=phi0+float(np)*stepphi

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
	t.setDir(outdir)
	t.setWL(1.0)
	t.setDataName(prefix)
	t.setCameraLength(cameralength)
	t.setOffset(serial_offset)
	t.setExpTime(0.1)
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

	for i in range(0,np,1):
		phi2=phi0+float(i)*stepphi
		each_vec=startvec+float(i)*mvec
		ofile.write("%12.5f %12.5f %12.5f %8.1f\n"%(each_vec[0],each_vec[1],each_vec[2],phi2))
		# mm unit
		mm_vec=each_vec/1000.0
		x,y,z=mm_vec[0],mm_vec[1],mm_vec[2]
		# mm unit
		mm_vec=each_vec/1000.0
		x,y,z=mm_vec[0],mm_vec[1],mm_vec[2]

		logstr="PHI=%6.1f CROSS"%phi2
		printVec(each_vec,logstr)
		#time.sleep(0.2)

	print "Total points:",n_total

# This crystal : points
print "N points/crystal=",n_points
collection_time=n_points*5.0/60.0 #[min]
centering_time=10 #[min]
time_cycle=collection_time+centering_time
print "Time for this crystal=",time_cycle,"[min]"
TotalTime+=time_cycle
	
print "1TIME:",TotalTime/60.0, " 2TIME:",TotalTime/30.0
