import sys,os,math,numpy
import Device
import Raddose
import BeamsizeConfig
import datetime
import Flux

nowt=datetime.datetime.now()
datepart=nowt.strftime("%y%m%d")
filename="fluxfactor-%s.dat"%datepart

of=open(filename,"w")

# Default configure file path
config_dir="/isilon/blconfig/bl32xu/"
bsc=BeamsizeConfig.BeamsizeConfig(config_dir)

if sys.argv[1]!="":
	print sys.argv[1]
        bsc.setConfigFile(sys.argv[1])
else:
	bsc=BeamsizeConfig.BeamsizeConfig(config_dir)

bsc.readConfig()
tw,th,bs,ff=bsc.getBeamParamList()

#dev=Device.Device("192.168.163.1")
dev=Device.Device("172.24.242.41")
dev.init()

# Prep scan
dev.prepScan()

# E=12.3984 keV 
# 2.72924+09 photons/1uA
en=12.3984

# Beam size change -> Dose estimation
energy_list = [10.0, 11.0, 12.0, 12.3984, 13, 14, 15]
hbeam_list=[]
vbeam_list=[]
flux_list=[]
for tcs_width,tcs_height,beamsize,ff in zip(tw,th,bs,ff):
	beam_index,h_beam,v_beam=beamsize
	dev.tcs.setApert(tcs_height,tcs_width)
	ipin,iic=dev.countPin(pin_ch=3)
	pin_uA=ipin/100.0
	iic_nA=iic/100.0
	fl=Flux.Flux(en)
	photon_flux=fl.calcFluxFromPIN(pin_uA)
	flux_list.append(photon_flux)
	rrr=Raddose.Raddose()
	dose_1sec=rrr.getDose(h_beam,v_beam,photon_flux,1.0,energy=en,remote=False)
	exp_for_10MGy=10.0/dose_1sec
	of.write("Beam %5.1f(v) x %5.1f(h) IC=%7.1f nA PIN=%8.2f uA %8.2e phs/sec Dose[10MGy]/sec= %5.2f sec\n" \
		%(v_beam,h_beam,iic_nA,pin_uA,photon_flux,exp_for_10MGy))
	of.flush()

	if tcs_width==0.1 and tcs_height==0.1:
		flux_base=photon_flux

dev.finishScan()

ofile=open("beamsize.config.%s"%datepart,"w")

for tcs_width,tcs_height,beamsize,flux in zip(tw,th,bs,flux_list):
	beam_index,h_beam,v_beam=beamsize
	h_beam_mm=h_beam/1000.0
	v_beam_mm=v_beam/1000.0
	ofile.write("_beam_size_begin:\n")
	ofile.write("_label: [h %4.1f x v %4.1f um]\n"%(h_beam,v_beam))
	# For flux factor
	if tcs_width==0.1 and tcs_height==0.1:
		ofile.write("_baseflux: [%8.1e]\n"%(flux))
	ofile.write("_outline: [rectangle %6.4f %6.4f 0.0 0.0 ]\n"%(h_beam_mm,v_beam_mm))
	ofile.write("_object_parameter: tc1_slit_1_width %5.3f mm\n"%tcs_width)
	ofile.write("_object_parameter: tc1_slit_1_height %5.3f mm\n"%tcs_height)
	ff=flux/flux_base
	ofile.write("_flux_factor: %8.4f\n"%ff)
	ofile.write("_beam_size_end:\n\n")
	ofile.flush()

ofile.close()
