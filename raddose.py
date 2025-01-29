import sys,os,math,time,tempfile,datetime
import Raddose

if __name__=="__main__":
	e=Raddose.Raddose()
	# 160509 wl=1.0A 10x15 um
	paramlist=[(9.0,3.92E11),(10.5,6.85E11),(12.4,8.09E11),(13.0,8.52E11),(15.5,7.7E11),(17.0,7.29E11),(18.0,6.44E11)]

	exptime=1.0
	for param in zip(paramlist):
		for en,flux in param:
			print en,flux
			#dose=e.getDose(15,9,1.04E13,exptime,energy=en)
			dose=e.getDose(4,3,flux,exptime,energy=en)
			exptime_to_10MGy=10.0/dose
			print "oxidase: %8.1f %8.3f MGy/sec Exptime(10MGy)=%6.2f"%(en,dose,exptime_to_10MGy)
