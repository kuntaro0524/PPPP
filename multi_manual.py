import os,sys
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

	# Camera distance selection
	##
	# TLN edge 1.8A
	##
	#dist=105.0 #E=8.5keV
	#dist=182.0 #E=12.3984keV
	#dist=145.0 #E=10.500keV
	#dist=225.0 #E=15.000keV
	#dist=282.0 #E=18.0keV
	#dist=220.0 #E=18.0keV high reso
	dist=120.0 #E=10.500keV

	## Attenetor
	#att_low=3000 # <=3000um #18.0keV
	#att_low=1200 # 12.3984keV
	att_low=700 # 10.5keV 
	#att_low=400 # 8.5keV 
	#att_low=1900 # 15.0keV (1.7%)

	## Exposure
	exp_low=1.0
	att_high=0
	exp_high=2.0

	## Wavelength
	#wl=0.6888   #18keV
	#wl=0.826560 #15.000 keV
	#wl=1.0000   #12.3984 keV
	wl=1.18080 #10.5 keV
	#wl=1.45863 #8.5keV


	ntimes=2
        #list=[(0.0669,    -14.5516 ,     0.4109), (0.0569,    -14.5666 ,     0.3936),(0.0469,    -14.5216 ,     0.3763)]#18keV
        #list=[(0.0769,    -14.6266 ,     0.4282),(0.0569,    -14.5366 ,     0.3936),(0.0569,    -14.6866 ,     0.3936)] # 15keV
        #list=[(0.0769,    -14.5966,      0.4282 ), (0.0669,    -14.6416,      0.4109 ), (0.0569,    -14.6566,      0.3936 )] # 12.3984keV
        #list=[(0.0769,    -14.5666,      0.4282),(0.0669,    -14.6116,      0.4109),(0.0569,    -14.6266,      0.3936)] # 10.5keV
        #list=[(0.0869,    -14.5966  ,    0.4455 ), (0.0669  ,  -14.5816   ,   0.4109 ), (0.0569 ,   -14.5966  ,    0.3936 )] # 8.5keV
        #list=[(0.0469,    -14.5516,      0.3763), (0.0469,    -14.5816,      0.3763), (0.0469,    -14.6116,      0.3763)] # 18keV x 2
        #list=[(0.0469,    -14.7016,      0.3763 ), (0.0369,    -14.5066,      0.3590 ), (0.0369,    -14.5366,      0.3590 )] # 18keV x 3
        list=[(0.0369,    -14.5966,      0.3590), (0.0369,    -14.6266,      0.3590), (0.0369,    -14.6566,      0.3590)] # 10.5 x 2

	idx=0
	xyzi=0
	cen=[]
	for cen in list:
		for offset in offset_list:
			h_off=offset[0]
			v_off=offset[1]
			newxyz=moveHV(cen,h_off,v_off,phi)
			print idx,newxyz
			idx+=1
			prefix="%03d_%03d"%(idx,xyzi)
			dire="%s/%02d/"%(curr_dir,xyzi)
        		# condition setting
        		mpr.setCenter(newxyz)
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
