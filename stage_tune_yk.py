import sys,os,math
import socket
from Count import *
from MyException import *
from File import *
import Device

# Make sure pin photodiode is swithced to No. 3 signal cable

if __name__=="__main__":
	host = '172.24.242.41'
	dev=Device.Device(host)
	dev.init()

	f=File("./")

	# Making log file for stage tuning
	fname="%03d_stagetune.log"%f.getNewIdx3()
	ofile=open(fname,"w")
	
	# Set Attenuator to 600um to scan diffractometer stage
	dev.setAttThick(600.0)

	# preparation of diffractometer scan
	dev.prepScanCoaxCam()

	# Get current YZ positions of diffractometer
	curr_sty=dev.stage.getYmm()
	curr_stz=dev.stage.getZmm()

	ofile.write("Sty=%12.5f Stz=%12.5f\n"%(curr_sty,curr_stz))

	# Scan
	fwhm_ymm,center_ymm=dev.stage.scanY("MOVE")
	fwhm_zmm,center_zmm=dev.stage.scanZ("MOVE")

	ofile.write("position Sty=%12.5f Stz=%12.5f\n"%(center_ymm,center_zmm))
	ofile.write("diameter Sty=%12.5f Stz=%12.5f\n"%(fwhm_ymm,fwhm_zmm))

	# Make sure 
	ofile.close()
