import sys, os, math, numpy
import Device_200929
import Raddose
import BeamsizeConfig
import datetime
import Flux

nowt = datetime.datetime.now()
datepart = nowt.strftime("%y%m%d")
filename = "fluxfactor-%s.dat" % datepart

of = open(filename, "w")

# Default configure file path
config_dir = "/isilon/blconfig/bl32xu/"
bsc = BeamsizeConfig.BeamsizeConfig(config_dir)

bsc.readConfig()
tw, th, bs, ff = bsc.getBeamParamList()

dev = Device_200929.Device("172.24.242.41")
dev.init()

# E=12.3984 keV
# 2.72924+09 photons/1uA
en = 12.3984

# Beam size change -> Dose estimation
wave_list = [1.4, 1.3, 1.2, 1.1, 1.0, 0.9, 0.8, 0.7]
#wave_list = [1.0]
flux_list = []

dev.finishScan()

flux_list = []
for wl in wave_list:
    en = 12.3984 / wl
    dev.changeEnergy(en, isTune=True, logpath="/isilon/BL32XU/BLsoft/PPPP/Logs/")
    # Prep scan
    dev.prepScan()

    for tcs_width, tcs_height, beamsize in zip(tw, th, bs):
        beam_index, h_beam, v_beam = beamsize
        dev.tcs.setApert(tcs_height, tcs_width)
        ipin, iic = dev.countPin(pin_ch=3)
        pin_uA = ipin / 100.0
        iic_nA = iic / 100.0
        fl = Flux.Flux(en)
        photon_flux = fl.calcFluxFromPIN(pin_uA)
        rrr = Raddose.Raddose()
        dose_1sec = rrr.getDose(h_beam, v_beam, photon_flux, 1.0, energy=en, remote=False)
        print "dose_1sec", dose_1sec
        exp_for_10MGy = 10.0 / float(dose_1sec)
        of.write(
            "wave = %9.5f Beam %5.1f(v) x %5.1f(h) IC=%7.1f nA PIN=%8.2f uA %8.2e phs/sec Dose[10MGy]/sec= %5.2f sec\n" \
            % (wl, v_beam, h_beam, iic_nA, pin_uA, photon_flux, exp_for_10MGy))
        flux_list.append((wl, v_beam, h_beam, photon_flux))
        of.flush()

    dev.closeShutters()

ofile = open("beamsize.config.%s" % datepart, "w")

linestr = "_wavelength_list:"

for wl in wave_list:
    linestr += "%5.3f," % wl

ofile.write("%s\n" % linestr[:-1])

for tcs_width, tcs_height, beamsize in zip(tw, th, bs):
    beam_index, h_beam, v_beam = beamsize
    h_beam_mm = h_beam / 1000.0
    v_beam_mm = v_beam / 1000.0
    ofile.write("_beam_size_begin:\n")
    ofile.write("_label: [h %4.1f x v %4.1f um]\n" % (h_beam, v_beam))
    ofile.write("_outline: [rectangle %6.4f %6.4f 0.0 0.0 ]\n" % (h_beam_mm, v_beam_mm))
    ofile.write("_object_parameter: tc1_slit_1_width %5.3f mm\n" % tcs_width)
    ofile.write("_object_parameter: tc1_slit_1_height %5.3f mm\n" % tcs_height)
    linestr = "_flux_list: "
    for wave in wave_list:
        for params in flux_list:
            wv, vb, hb, photon_flux = params
            if wv == wave and vb == v_beam and hb == h_beam:
                linestr += " %5.3e," % photon_flux
    ofile.write("%s\n" % linestr[:-1])
    ofile.write("_beam_size_end:\n\n")
    ofile.flush()

ofile.close()
