import os,sys
sys.path.append("/isilon/BL32XU/BLsoft/PPPP/")
from MultiPointRD import *
from numpy import *
from Gonio import *
from Resolution import *
from Att import *

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

	if len(sys.argv)!=2:
		print "Usage: this GONIOFILE"
		sys.exit(1)


        mpr=MultiPointRD()
	rescalc=Resolution()
	att=Att(s)
        curr_dir=os.environ['PWD']

	# Condition
	offset_list=[(0.0,0.0)]
	stepphi=0.1

	# setting list file is to be read
	inpfile=open(sys.argv[1],"r")
	inlines=inpfile.readlines()

	###########################################
	# Beam size for probe and burn in [um]
	###########################################
	probe_h,probe_v=1,10
	burn_v=10
	npoints=31


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
		# Gonio rotation
		phi=float(cols[3])
		startphi=phi
		endphi=phi+stepphi
		# energy
		enstr="%skeV"%cols[4]
		en=float(cols[4])
		wl=round(12.3984/en,5)
		burn_h=float(cols[5])
		max_dose=float(cols[6])

		# step of probe measurements
		if burn_h==1.0:
			step=0.0005
		elif burn_h==2.0:
			step=0.0005
		elif burn_h==5.0:
			step=0.001
		elif burn_h==10.0:
			step=0.0015

		print max_dose,"[MGy]"
		print "Beam size for Burned",burn_h,"[um]"

	#########################################
	### Setting
	#########################################
		# Aimed resolution
		resol=1.80
		# Aimed dose
		objective_dose=30.0 # MGy
		# Aimed low dose percentage
		ld_percent=2.0
		
	######################
	### Automatic condition but modify max_dose for each energy
	######################
		if en==12.3984:
			# Exposure time[sec]
			att_high=0
			exp_high=round(objective_dose/max_dose,2)
			#=== CL ===#
			rescalc.setWL(wl)
			dist=rescalc.getDistResol(resol)
			#=== Low dose exposure ====#
			low_trans=exp_high*ld_percent/100.0
			att_low,exp_low=att.getBestExpCondition(wl,low_trans)

		elif en==18.0:
			# Exposure time[sec]
			att_high=0
			exp_high=round(objective_dose/max_dose,2)
			#=== CL ===#
			rescalc.setWL(wl)
			dist=rescalc.getDistResol(resol)
			#=== Low dose exposure ====#
			low_trans=exp_high*ld_percent/100.0
			att_low,exp_low=att.getBestExpCondition(wl,low_trans)

		elif en==15.5:
			# Exposure time[sec]
			att_high=0
			exp_high=round(objective_dose/max_dose,2)
			#=== CL ===#
			rescalc.setWL(wl)
			dist=rescalc.getDistResol(resol)
			#=== Low dose exposure ====#
			low_trans=exp_high*ld_percent/100.0
			att_low,exp_low=att.getBestExpCondition(wl,low_trans)

		elif en==10.5:
			# Exposure time[sec]
			att_high=0
			exp_high=round(objective_dose/max_dose,2)
			#=== CL ===#
			rescalc.setWL(wl)
			dist=rescalc.getDistResol(resol)
			#=== Low dose exposure ====#
			low_trans=exp_high*ld_percent/100.0
			att_low,exp_low=att.getBestExpCondition(wl,low_trans)

		elif en==8.5:
			# Exposure time[sec]
			att_high=0
			exp_high=round(objective_dose/max_dose,2)
			#=== CL ===#
			rescalc.setWL(wl)
			dist=rescalc.getDistResol(resol)
			#=== Low dose exposure ====#
			low_trans=exp_high*ld_percent/100.0
			att_low,exp_low=att.getBestExpCondition(wl,low_trans)

		#print "#####"
		#print en,dist,att_low,att_high,exp_low,exp_high
		#print cen,gx,gy,gz,en,wl
		#print "#####"

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
       		mpr.genSchefile(dire,prefix,probe_h,probe_v,burn_h,burn_v)
		xyzi+=1
