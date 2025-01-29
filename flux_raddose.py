import sys,os,math,numpy
import Device
import Raddose
import BeamsizeConfig
import datetime

nowt=datetime.datetime.now()
filename=nowt.strftime("%y%m%d")+".dat"

of=open(filename,"w")

config_dir="/isilon/blconfig/bl32xu/"
bsc=BeamsizeConfig.BeamsizeConfig(config_dir)
bsc.readConfig()
tw,th,bs,ff=bsc.getBeamParamList()

#dev=Device.Device("192.168.163.1")
dev=Device.Device("172.24.242.41")
dev.init()

# E=12.3984 keV 
# 2.72924+09 photons/1uA
en=12.3984

# Beam size change -> Dose estimation
hbeam_list=[]
vbeam_list=[]
for tcs_width,tcs_height,beamsize,ff in zip(tw,th,bs,ff):
	beam_index,h_beam,v_beam=beamsize
	dev.tcs.setApert(tcs_height,tcs_width)
	ipin,iic=dev.countPin(pin_ch=3)
	pin_uA=ipin/100.0
	iic_nA=iic/100.0
	photon_flux=2.72924E9*pin_uA
	rrr=Raddose.Raddose()
	dose_1sec=rrr.getDose(h_beam,v_beam,photon_flux,1.0,energy=en)
	exp_for_10MGy=10.0/dose_1sec
	of.write("Beam %5.1f(v) x %5.1f(v) IC=%7.1f nA PIN=%8.2f uA %8.2e phs/sec Dose/sec= %5.2f sec\n" \
		%(v_beam,h_beam,iic_nA,pin_uA,photon_flux,exp_for_10MGy))
