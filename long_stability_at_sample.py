from Stage import *
from Shutter import *
from File import *
from ExSlit1 import *
from Light import *
from numpy import *
from Gonio import *
from Mono import *
from Colli import *
from ID import *
import socket

if __name__=="__main__":
        host = '172.24.242.41'
        port = 10101
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host,port))

	# Required equipments
	slit1=ExSlit1(s)
	shutter=Shutter(s)
	light=Light(s)
	f=File(".")
	gonio=Gonio(s)
	mono=Mono(s)
	tcs=TCS(s)
	colli=Colli(s)
	id=ID(s)

	# Slit1 open
        light.off()
        slit1.openV()
        shutter.open()

	# File
	logfile=open("intensity.dat","w")
	
	# change energy
	en=12.3984
	mono.changeE(en)
	id.moveE(en)

	counter=Count(s,3,0)

	starttime=time.time()
	for i in range(0,12): # hours
	# dtheta1 tune
		detune=-50
		prefix="%03d"%(f.getNewIdx3())
		dt1peak=1.0
		#fwhm,dt1peak=mono.scanDt1PeakConfigExceptForDetune(prefix,"DTSCAN_NORMAL",tcs,detune)
                ch1,ch2=counter.getCount(1.0)
		currtime=time.time()
		ttime=currtime-starttime
		logfile.write("Just after dt1 tune %8.3f %7.4f %5.1f %8.1f\n"%(ttime,en,dt1peak,ch2))
		logfile.flush()

		# check stability
		for j in range(0,18): # 10 mins x 18 = 3 hours
        		slit1.openV()
                	ch1,ch2=counter.getCount(1.0)
			currtime=time.time()
			ttime=currtime-starttime
			logfile.write("%8.3f %7.4f %5.1f %8.1f\n"%(ttime,en,dt1peak,ch2))
			logfile.flush()
        		slit1.closeV()
			print "waiting for 600 seconds"
			time.sleep(600)

        shutter.close()
        slit1.closeV()
