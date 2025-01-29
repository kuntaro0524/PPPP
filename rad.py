import sys,os,math
import EstimateDose

if __name__=="__main__":
	e=EstimateDose.EstimateDose()

	wl=1.0
	en=12.3984/wl
	phs=1.0E13
	dose_1sec=e.getDose(10,15,phs,1.0,energy=en)
	print "%8.5f[A] 10x15 um beam %5.2e phs/sec Dose= %5.3f MGy/sec"%(wl,phs,dose_1sec)

	wl=1.28
	en=12.3984/wl
	phs=6.52E12
	dose_1sec=e.getDose(10,15,phs,1.0,energy=en)
	print "%8.5f[A] 10x15 um beam %5.2e phs/sec Dose= %5.3f MGy/sec"%(wl,phs,dose_1sec)

	wl=1.35
	en=12.3984/wl
	phs=5.53E12
	dose_1sec=e.getDose(10,15,phs,1.0,energy=en)
	print "%8.5f[A] 10x15 um beam %5.2e phs/sec Dose= %5.3f MGy/sec"%(wl,phs,dose_1sec)

	wl=1.40
	en=12.3984/wl
	phs=4.79E12
	dose_1sec=e.getDose(10,15,phs,1.0,energy=en)
	print "%8.5f[A] 10x15 um beam %5.2e phs/sec Dose= %5.3f MGy/sec"%(wl,phs,dose_1sec)

	wl=1.45
	en=12.3984/wl
	phs=3.95E12
	dose_1sec=e.getDose(10,15,phs,1.0,energy=en)
	print "%8.5f[A] 10x15 um beam %5.2e phs/sec Dose= %5.3f MGy/sec"%(wl,phs,dose_1sec)
