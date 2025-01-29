import sys,os,math,time,tempfile,datetime
import Raddose

if __name__=="__main__":
	e=Raddose.Raddose()

	wavelength=float(sys.argv[1])
	flux=float(sys.argv[2])
	vbeam=float(sys.argv[3])
	hbeam=float(sys.argv[4])

	en=12.3984/wavelength

	dose=e.getDose(vbeam,hbeam,flux,1.0,energy=en)
	print "1sec dose=",dose, " MGy"
	exptime_to_10MGy=10.0/dose
	print "10MGy exptime=",exptime_to_10MGy
