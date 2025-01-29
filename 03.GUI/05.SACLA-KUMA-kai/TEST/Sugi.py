import sys,os
import All
import numpy as np
import Schedule_HSS_Re

if __name__ == '__main__':
	# Experimental conditions
	#wl=12.3984/10.02
	wl=1.0
	cl=130.0
	prefix="test"
	step_size=0.05
	phi=0.0
	phistep=0.2
	
	# Normal square 
	a=np.array([0.0,  0.5,  0.2])
	b=np.array([0.0,  0.5,  0.00])
	c=np.array([0.1,  0.0,  0.00])
	d=np.array([0.1,  0.0,  0.2])

	# Read from file
	lines=open(sys.argv[1],"r").readlines()
	glist=[]
	for line in lines:
		if line=="\n":
			continue
		else:
			cols=line.split()
			if cols[0]=="#":
				continue
			else:
				phireal=float(cols[0])
				phipres=float(cols[1])
				gx=float(cols[2])
				gy=float(cols[3])
				gz=float(cols[4])
				xyz=np.array([gx,gy,gz])
				glist.append(xyz)
	a=glist[0]
	b=glist[1]
	c=glist[2]
	d=glist[3]

	print a,b,c,d
	print phireal

	all=All.All(a,b,c,d,phireal,step_size,phistep)
	irrad_vecs=all.horizontalType(phireal)

	np=0
	serial_offset=0
	for vecinfo in irrad_vecs:
		svec,evec,adv_step,npoints,curr_phi=vecinfo
		print "ADV_STEP:",adv_step
		schedule_file="test%03d.sch"%np

		# BSS deha npoints+1 ni subeki?
		npoints=npoints+1

		################################
		# Setting parameters to 
		################################
		# Static parameters
		#class Schedule_HS_Re:
		t=Schedule_HSS_Re.Schedule_HSS_Re()
		#class Schedule_HS_Re:

		dd="/isilon/users/target/target/Staff/150619/ProgCheck/"
		t.setDir(dd)
		t.setWL(wl)
		t.setDataName(prefix)
		t.setCameraLength(cl)
		t.setOffset(serial_offset)
		t.setExpTime(1.0)
		adv_step_um=adv_step*1000.0
		t.sfrox(svec,evec,curr_phi,phistep,npoints,adv_step_um)
		t.setAttIdx(0)
		t.setScanInt(1)
		t.make(schedule_file)

		serial_offset+=npoints
		np+=1
