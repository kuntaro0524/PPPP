from RotationCenter import *
from File import *
from Gonio import *
from Capture import *
from Light import *
import math
from Zoom import *
import datetime

if __name__=="__main__":

	rc=RotationCenter()

	starttime=datetime.datetime.now()

	of=open("rotation_center.log","w")
	of.write("# TIME CONSTIME[min] GX GY GZ (saved GX GY GZ) DIST_BEFORE_AFTER TIMES_TO_CENTER\n")
	of.flush()
### PORT
	#host = '192.168.163.1'
	host = '172.24.242.41'
	port = 10101
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host,port))
### PORT
	gonio=Gonio(s)
	f=File("./")

	sx,sy,sz=gonio.getXYZmm()
	of.write("# Saved gonio position %12.5f%12.5f%12.5f\n"%(sx,sy,sz))
	of.flush()

	while(1):
		# Initialization of flags
		isOkay1=False
		isOkay2=False
		isOkay3=False
		ntimes=0

		while(1):
			ntimes+=1
			if isOkay1==False:
				print " 0-180 deg"
				d1,c1=rc.tuneGonioAve(0,180)
			if isOkay2==False:
				print " 90-270 deg"
				d2,c2=rc.tuneGonioAve(90,270)
			if isOkay3==False:
				print " 45-225 deg"
				d3,c3=rc.tuneGonioAve(45,225)
			if fabs(d1)<0.3:
				isOkay1=True
			if fabs(d2)<0.3:
				isOkay2=True
			if fabs(d3)<0.3:
				isOkay3=True
			if isOkay1==True and isOkay2==True and isOkay3==True:
				break

		# Kinen satsuei
		kinen_pic="%s/%03d_kinen.ppm"%(f.getAbsolutePath(),f.getNewIdx3())

		# Final position
		sumc=0.0
		for i in range(0,5):
			rc.captureOnly(kinen_pic)
			# Kinen center
			fwhm,center=rc.capAna(kinen_pic)
			sumc+=center
		final_cen=sumc/5.0
		rc.finish()

		curr_time=datetime.datetime.now()
		time_from_start=(curr_time-starttime).seconds

		xa,ya,za=gonio.getXYZmm()
		dx=sx-xa
		dy=sy-ya
		dz=sz-za

		# Distance from initial position
		dist=math.sqrt(dx*dx+dy*dy+dz*dz)
		of.write("%s %10.1f %8.2f %8.2f %8.2f %8.2f (%12.5f%12.5f%12.5f) %8.3f %2d\n"%
			(curr_time,time_from_start,c1,c2,c3,final_cen,xa,ya,za,dist,ntimes))
		of.flush()

		## Evacuation of needle position ##
		print "Evacuate for avoiding ice weight"
		gonio.moveTrans(5000)
		tx,ty,tz=gonio.getXYZmm()
		print "EVAC",tx,ty,tz

		## Wait for 60 mins
		gonio.rotatePhi(0.0)
		print "Wait for 1 hour....: %s"%curr_time
		time.sleep(3600)

		## Preparation for the next run ###
		print "Recovering the goniometer position for the next run"
		gonio.moveTrans(-5000)
		tx,ty,tz=gonio.getXYZmm()
		# For instant thermal-equilibrium
		time.sleep(60)

	of.close()
