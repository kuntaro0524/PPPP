import sys
import socket
import time
import math
from pylab import *
import numpy

# My library
from AnalyzePeak import *
from File import *
from Enc import *
from Gonio import *

if __name__=="__main__":
	#host = '192.168.163.1'
	host = '172.24.242.41'
	port = 10101
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host,port))

	gonio=Gonio(s)
	f=File("./")

	# wait time
	wait=0.1
	sx,sy,sz=gonio.getXYZmm()

	# Gonio phi list
	#phi_list=[0.0,45.0,90.0,135.0,180.0]
	phi_list=[0.0]

	#gonio.prepScan()
	move_width=100.0 # [um]
	move_step=10.0 #[um]

	for i in arange(1,2):
		for phi in phi_list:
			gonio.rotatePhi(phi)
			for sense in [1.0,-1.0]:
			#for sense in [1.0]:
				# File name
				fname="%03d_phi_%f_sense_%f_gonio_enc.scn"%(f.getNewIdx3(),phi,sense)
				ofile=open(fname,"w")
				start_position=move_width*sense
				gonio.moveUpDown(start_position)
				this_step=move_step*sense*-1.0
				ofile.write("# START = %8.3f STEP= %8.3f\n"%(start_position,this_step))
				nobs=int(move_width/move_step)*2
	
				for idx in arange(0,nobs,1):
					gonio.moveUpDown(this_step)
					time.sleep(wait)
					px,py,pz=gonio.getXYZmm()
					ex,ey,ez=gonio.getEnc()
					diff_x=px-ex
					diff_y=py-ey
					diff_z=pz-ez
					ofile.write("PHI= %6.1f PLS: %12.5f %12.5f %12.5f ENC: %12.5f %12.5f %12.5f DIFF: %12.5f %12.5f %12.5f\n"%(phi,px,py,pz,ex,ey,ez,diff_x,diff_y,diff_z))
					ofile.flush()
				gonio.moveXYZmm(sx,sy,sz)
				ofile.close()
	s.close()
