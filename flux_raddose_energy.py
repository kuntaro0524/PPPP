import sys,os,math,numpy
import Device
import Raddose
import BeamsizeConfig
import datetime
import Flux

nowt=datetime.datetime.now()
filename=nowt.strftime("%y%m%d-%H%M")+".dat"

of=open(filename,"w")

config_dir="/isilon/blconfig/bl32xu/"
bsc=BeamsizeConfig.BeamsizeConfig(config_dir)
bsc.readConfig()
tw_list,th_list,bs_list,ff_list=bsc.getBeamParamList()

#dev=Device.Device("192.168.163.1")
dev=Device.Device("172.24.242.41")
dev.init()

en_list=[8.5,15.0]

# dtheta1 skip?
# Normally False
dt1tune_skip=False

for en in en_list:
	# Dtheta1 tuning
        dev.finishScan(cover_off=False)
	# Energy change
    	dev.mono.changeE(en)
	# Gap 
    	dev.id.moveE(en)
	# dtheta tune 
	if dt1tune_skip==False:
        	prefix="%03d"%dev.f.getNewIdx3()
        	dev.mono.scanDt1PeakConfig(prefix,"DTSCAN_NORMAL",dev.tcs)
        	dtheta1=int(dev.mono.getDt1())
        	print "Final dtheta1 = %d pls"%dtheta1
	# Prep PIN on the diffractometer
	dev.prepScan()

	for tcs_width,tcs_height,beamsize,ff in zip(tw_list,th_list,bs_list,ff_list):
		dev.slit1.openV()
		beam_index,h_beam,v_beam=beamsize
		dev.tcs.setApert(tcs_height,tcs_width)
		ipin,iic=dev.countPin(pin_ch=3)
		pin_uA=ipin/100.0
		iic_nA=iic/100.0
		# Photon flux estimation
                ff=Flux.Flux(en)
        	phosec=ff.calcFluxFromPIN(pin_uA)
		rrr=Raddose.Raddose()
		dose_1sec=rrr.getDose(h_beam,v_beam,phosec,1.0,energy=en)
		exp_for_10MGy=10.0/dose_1sec
		of.write("En=%9.4f %5.1f(v) x %5.1f(v) IC=%7.1f nA PIN=%8.2f uA %8.2e phs/sec Dose/sec= %5.2f sec\n" %(en,v_beam,h_beam,iic_nA,pin_uA,phosec,exp_for_10MGy))
