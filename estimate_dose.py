import os,sys,math
import Raddose
import AttFactor

if __name__=="__main__":
        e=Raddose.Raddose()

	print "Usage: hbeam vbeam exp_time nframes att_thick wavelength"

	flux_density=7E10
	hbeam=float(sys.argv[1])
	vbeam=float(sys.argv[2])
	exp_time=float(sys.argv[3])
	nframes=int(sys.argv[4])
	att_thick=float(sys.argv[5])
	wavelength=float(sys.argv[6])

	en=12.3984/wavelength

        flux=flux_density*hbeam*vbeam #photons/sec

        att=AttFactor.AttFactor()
        attfac=att.calcAttFac(wavelength,att_thick)
	print "Att factor=",attfac

	flux_att=attfac*flux
	print "%8.3e"%flux_att

        dose=e.getDose(hbeam,vbeam,flux_att,exp_time,energy=en,remote=False)
	print "Dose/frame  =%5.2f MGy"%dose
	print "Dose/dataset=%5.2f MGy"%(dose*nframes)
        #print "%8.1f %8.3f MGy (oxidase)"%(en,dose)
