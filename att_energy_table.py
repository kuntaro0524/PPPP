from numpy import *
import Device
import socket,time
import AttFactor

if __name__=="__main__":
        host = '172.24.242.41'
	dev=Device.Device(host)
	dev.init()

	# Energy list
	en=12.3984
	#dev.finishScan()

	attfac=AttFactor.AttFactor()
	thick_list,idx_list,pulse_list=attfac.getList()

	# File
	oname="att_pulse.scn"
	ofile=open(oname,"w")
	# change energy
	dev.mono.changeE(en)
	dev.id.moveE(en)

	# dTheta Tune
	#dtheta_fwhm,dtheta_center=dev.mono.scanDt1PeakConfigExceptForDetune(prefix,"DTSCAN_NORMAL",tcs,detune)

	# Prep scan on diffractometer
	dev.prepScan()

	# Att 0 intensity
	i0,ic0=dev.countPin()

	ofile.write("I0=%12.5f \n"%i0)

	idx=0
	for thick,pulse in zip(thick_list,pulse_list):
		print "Moving to %5d"%pulse
		dev.att.move(int(pulse))
		cnt,ic=dev.countPin()
		trans=float(cnt)/float(i0)
		ofile.write("%8.2f  %5d  %10.5f\n"%(float(thick),pulse,trans))
		print "%8.2f  %5d  %10d %10.5f"%(float(thick),pulse,cnt,trans)
		ofile.flush()
	ofile.close()

	dev.closeAllShutter()
