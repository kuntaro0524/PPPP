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

	sx,sy,sz=gonio.getXYZmm()
	colli.off()

	# Slit1 open
        light.off()
        slit1.openV()
        shutter.open()

	# Energy list
	en_list=arange(8.6,20.1,0.4)

	# File
	logfile=open("Table.dat","w")
	for en in en_list:
		# change energy
		mono.changeE(en)
		id.moveE(en)

		# dtheta1 tune
		if en <= 10.0:
			detune=-200
			prefix="%03d_%07.4fkeV"%(f.getNewIdx3(),en)
			mono.scanDt1PeakConfigExceptForDetune(prefix,"DTSCAN_NORMAL",tcs,detune)

		elif en > 10.0:
			detune=-50
			prefix="%03d_%7.4fkeV"%(f.getNewIdx3(),en)
			mono.scanDt1PeakConfigExceptForDetune(prefix,"DTSCAN_NORMAL",tcs,detune)

		# Needle set position
		gonio.moveXYZmm(sx,sy,sz)

		# Scan stage with needle
        	prefix="%03d_%07.4fkeV"%(f.getNewIdx3(),en)
        	junk,stz_value=stage.scanZneedleMove(prefix,0.002,40,3,0,0.2)

		# Collimator scan without needle
		gonio.moveTrans(1000.0)
        	prefix="%03d_%07.4fkeV_colli"%(f.getNewIdx3(),en)
        	ceny,cenz,fwhm_z,fwhm_y=colli.scanWithoutPreset(prefix,3)
        	trans,pin=colli.compareOnOff(3)
		colli.off()
		logfile.write("%7.4f %5d %6.4f %5d %5d %5.1f %5.1f %5.2f %10d"%(en,detune,stz_value,ceny,cenz,fwhm_y,fwhm_z,trans,pin))
		logfile.flush()

	gonio.moveXYZmm(sx,sy,sz)
	logfile.close()

        shutter.close()
        slit1.closeV()
