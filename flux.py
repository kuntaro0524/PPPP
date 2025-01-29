import sys,os,math,numpy
import Device

#dev=Device.Device("192.168.163.1")
dev=Device.Device("172.24.242.41")
dev.init()
#dev.setAttThick(0.0)

dev.prepScan()
#wavelength = 12.3984/dev.mono.getE()
wavelength = 12.3984/dev.mono.getE()

if len(sys.argv) != 2:
    print "Usage: input 'colli_on' or 'colli_off'"
    sys.exit()

if sys.argv[1] == "colli_on":
    dev.colli.on()
else:
    dev.colli.off()

dev.bsOff()
dev.openShutters()

ipin,iic=dev.countPin(pin_ch=3)

dev.closeShutters()

pin_uA=ipin/100.0
iic_nA=iic/100.0

# E=12.3984 keV 
# 2.72924+09 photons/1uA
photon_flux=2.72924E9*pin_uA

print "IC=%7.1f nA PIN=%8.2f uA %8.2e phs/sec"%(iic_nA,pin_uA,photon_flux)

