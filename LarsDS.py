from GonioVec import *
import socket
import Gonio
import ScheduleBSS_HS_SH
import time

if __name__=="__main__":
	#host = '192.168.163.1'
	host = '172.24.242.41'
	port = 10101
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host,port))

        gonio=Gonio.Gonio(s)
	t=ScheduleBSS_HS_SH.ScheduleBSS_HS_SH()
	print "Usage: python ~/PPPP/LarsDS.py LENGTH_HORIZONTAL[um] LENGTH_VERTICAL[um] EXPTIME[sec] OUTPUT_DIRECTORY"

# Input parameters
	veclen=float(sys.argv[1]) #[um] scan vector length of each line
	total_length_vertical=float(sys.argv[2])
	exp_time=float(sys.argv[3])

#############################################################################

############################
# ROTATION CONDITIONS
	phi=gonio.getPhi()
#	COnditions
	startphi=phi-45.0
	endphi=phi+46
	stepphi=1.0

	total_phi=endphi-startphi
	nframes=int(total_phi/stepphi)

############################
# Goniometer setting (COMMON)
############################
	adstep=veclen/float(nframes)
	print "Advanced step=",adstep,"[um]"
	interval=1

######################
# Starting vector "migi-ue hashi"
######################
        x,y,z=gonio.getXYZmm()
	svec=(x,y,z)

	veclen_mm=veclen/1000.0

# LOOP
	gap_between_line=30.0 #[um]

	# Vertical offset at this PHI[deg]
	dx,dz=gonio.calcUpDown(gap_between_line)
	nlines=int(total_length_vertical/gap_between_line)

	command="rm -f /tmp/ttt_lars???.sch"
	os.system(command)

	for i in range(0,nlines):
		# Starting point of this line
		sx=svec[0]+float(i)*dx
		sy=svec[1]
		sz=svec[2]+float(i)*dz
		lvec1=(sx,sy,sz)

		# End point of this line
		ex=sx
		ey=sy+fabs(veclen_mm)
		ez=sz
		lvec2=(ex,ey,ez)

		t.setDir(sys.argv[4])
		t.setCameraLength(300)
		t.setAttThickness(0)
		# Length in unit [um]
		t.stepAdvanced(lvec1,lvec2,adstep,1,startphi,stepphi,interval)
		t.setDataName("data_%03d"%i)
		t.setExpTime(exp_time)
		t.setWL(1.000)
		t.make("/tmp/ttt_lars%03d.sch"%i)

	# Making schedule file
	time.sleep(5)
	command="cat /tmp/ttt_lars???.sch > ~/all_lars.sch"
	os.system(command)

	s.close()
