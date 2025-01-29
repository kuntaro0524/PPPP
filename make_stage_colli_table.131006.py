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
import socket,time

from CCDlen import *
from Cover import *
from CMOS import *

if __name__=="__main__":
        host = '172.24.242.41'
        port = 10101
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host,port))

	# Required equipments
        stage=Stage(s)
	slit1=ExSlit1(s)
	shutter=Shutter(s)
	light=Light(s)
	f=File(".")
	gonio=Gonio(s)
	mono=Mono(s)
	tcs=TCS(s)
	colli=Colli(s)
	id=ID(s)

##### Modified by YK 121008
        clen=CCDlen(s)
        covz=Cover(s)
        cmos=CMOS(s)
##### Modified by YK 121008

	sx,sy,sz=gonio.getXYZmm()
	colli.off()

##### Modified by YK 121008
        ## CMOS off
        cmos.off()

        clen.evac()
        ## Cover on
        covz.on()
        print "CCD cover was closed"
        ## Cover check
        if covz.isCover():
		slit1.openV()
                print "Slit1 lower blade opened"
                light.off()
                print "Light went down"
                shutter.open()
                print "Shutter on diffractometer was opened"

	# Slit1 open
##        light.off()
##        slit1.openV()
##        shutter.open()
##### Modified by YK 121008

	# Energy list
	en_list=arange(8.5,20.1,0.3)

	# File
	logfile=open("Table.dat","w")
	logfile2=open("Table.tbl","w")
	for en in en_list:
		# change energy
		mono.changeE(en)
		id.moveE(en)

		# Sleep for thermal equilibrium (30mins)
		if en == 8.5:
			time.sleep(1800)

		# dtheta1 tune
		if en <= 10.0:
			detune=-200
			prefix="%03d_%07.4fkeV"%(f.getNewIdx3(),en)
##### Modified by YK 121008
#			mono.scanDt1PeakConfigExceptForDetune(prefix,"DTSCAN_NORMAL",tcs,detune)
			dtheta_fwhm,dtheta_center=mono.scanDt1PeakConfigExceptForDetune(prefix,"DTSCAN_NORMAL",tcs,detune)
##### Modified by YK 121008

		elif en > 10.0:
			detune=-50
			prefix="%03d_%7.4fkeV"%(f.getNewIdx3(),en)
##### Modified by YK 121008
#			mono.scanDt1PeakConfigExceptForDetune(prefix,"DTSCAN_NORMAL",tcs,detune)
			dtheta_fwhm,dtheta_center=mono.scanDt1PeakConfigExceptForDetune(prefix,"DTSCAN_NORMAL",tcs,detune)
##### Modified by YK 121008

		# Needle set position
		gonio.moveXYZmm(sx,sy,sz)

		# Scan stage with needle
		nsum=0
		sum=0.0
		for nrep in range(0,5):
        		prefix="%03d_%07.4fkeV"%(f.getNewIdx3(),en)
        		junk,stz_value=stage.scanZneedleMove(prefix,0.002,40,3,0,0.2)
			logfile.write("%12.5f "%stz_value)
			sum+=stz_value
			nsum+=1
		stz_value=sum/float(nsum)

		# Collimator scan without needle
		gonio.moveTrans(1000.0)
        	prefix="%03d_%07.4fkeV_colli"%(f.getNewIdx3(),en)
##        	ceny,cenz,fwhm_z,fwhm_y=colli.scanWithoutPreset(prefix,3)
        	ceny,cenz,fwhm_z,fwhm_y=colli.scanWithoutPreset(prefix,3,0.2)
        	trans,pin=colli.compareOnOff(3)
		colli.off()
		logfile.write("\n")
		logfile.write("%7.4f %5d %6.4f %5d %5d %5.1f %5.1f %5.2f %10d\n"%(en,detune,stz_value,ceny,cenz,fwhm_y,fwhm_z,trans,pin))
		logfile.flush()
##### Modified by YK 121008
		logfile2.write("%7.4f %5d %6.4f %5d %5d\n"%(en,dtheta_center,stz_value,ceny,cenz))
		logfile2.flush()
##### Modified by YK 121008

	gonio.moveXYZmm(sx,sy,sz)
	logfile.close()

        shutter.close()
        slit1.closeV()
