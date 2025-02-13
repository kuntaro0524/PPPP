import os,sys
sys.path.append("/isilon/BL32XU/BLsoft/PPPP/")
from MultiPointRD import *
from numpy import *
from Gonio import *

def moveHeight(inixyz,phi,height):
	finxyz=[1,2,3]
        # Up-down from current phi
        curr_phi=math.radians(phi)

        # unit [mm]
        move_x=-height*math.sin(curr_phi)
        move_z=height*math.cos(curr_phi)

        # marume[um]
        move_x=round(move_x,5)
        move_z=round(move_z,5)

	finxyz[0]=inixyz[0]+move_x
	finxyz[1]=inixyz[1]
	finxyz[2]=inixyz[2]+move_z

	return finxyz

def moveTrans(inixyz,trans):
	finxyz=[1,2,3]

        # marume[um]
        move_y=round(trans,5)

	finxyz[0]=inixyz[0]
	finxyz[1]=inixyz[1]+move_y
	finxyz[2]=inixyz[2]

	return finxyz

def moveHV(inixyz,h,v,phi):
	tmp=moveTrans(inixyz,h)
	tmp2=moveHeight(tmp,phi,v)

	return tmp2

if __name__=="__main__":
        host = '172.24.242.41'
        port = 10101
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host,port))

        mpr=MultiPointRD()
	gonio=Gonio(s)
	rescalc=Resol()
        curr_dir=os.environ['PWD']

	# Current status
	#cen=gonio.getXYZmm()
	phi=gonio.getPhi()

	# Condition
	offset_list=[(0.0,0.0)]
	startphi=phi
	stepphi=0.1
	endphi=phi+stepphi
	step=0.0005
	npoints=31

	# setting list file is to be read
	inpfile=open(sys.argv[1],"r")
	inlines=inpfile.readlines()
	
	# Scan number
	ntimes=2
	idx=0
	xyzi=0
	for line in inlines:
		# reading columns
		cols=line.split()
		# Gonio xyz
		gx=float(cols[0])
		gy=float(cols[1])
		gz=float(cols[2])
		cen=[gx,gy,gz]
		# energy
		enstr="%skeV"%cols[4]
		en=float(cols[4])
		wl=round(12.3984/en,5)

		#print enstr
#Aimed to 1.8A resolution
		# Aimed resolution
		resol=1.80
		# Aimed dose
		objective_dose=30.0 # MGy
		
		if en==12.3984:
			# Input information #
			#=== Dose/sec FF ====#
			max_dose=21.0 #MGy

			# Exposure time
			exp_high=round(objective_dose/max_dose,1)
			#=== CL ===#
			rescalc.setWL(wl)
			dist=rescalc.getDistResol(resol)
			#=== AL ==="
			att_low=1200
			att_high=0
			#=== Exposure time ==="
			exp_low=1.0
			exp_high=1.6 # 20MGy Thaumatin

		elif en==18.0:
			# Input information #
			#=== Dose/sec FF ====#
			max_dose=21.0 #MGy
                        #=== CL ===#
                        dist=280.0
                        #=== AL ==="
                        att_low=3000
                        att_high=0
                        #=== Exposure time ==="
                        exp_low=1.0
                        exp_high=4.0

		elif en==10.5:
			# Input information #
			#=== Dose/sec FF ====#
			max_dose=21.0 #MGy
                        #=== CL ===#
                        dist=105.0
                        #=== AL ==="
                        att_low=700
                        att_high=0
                        #=== Exposure time ==="
                        exp_low=1.0
                        exp_high=2.0

		elif en==8.5:
			# Input information #
			#=== Dose/sec FF ====#
			max_dose=21.0 #MGy

                        #=== CL ===#
                        dist=105.0

                        #=== AL ==="
                        att_low=400
                        att_high=0

                        #=== Exposure time ==="
                        exp_low=1.0
                        exp_high=2.2

		print "#####"
		print en,dist,att_low,att_high,exp_low,exp_high
		print cen,gx,gy,gz,en,wl
		print "#####"

		idx+=1
		prefix="%03d_%03d"%(idx,xyzi)
		dire="%s/%s/%02d/"%(curr_dir,enstr,xyzi)
       		# condition setting
       		mpr.setCenter(cen)
       		mpr.setScanCondition(startphi,endphi,stepphi)
       		mpr.setStep(step)
       		mpr.setNpoint(npoints)
       		mpr.setDist(dist)
       		mpr.setLow(att_low,exp_low)
       		mpr.setHigh(att_high,exp_high)
       		mpr.setWL(wl)
       		mpr.setNtime(ntimes)
       		mpr.genSchefile(dire,prefix)
		xyzi+=1
