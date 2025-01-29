import sys,os,math,numpy
import Device

dev=Device.Device("192.168.163.1")
dev.init()
dev.setAttThick(0.0)
dev.colli.on()

ipin,iic=dev.countPin(pin_ch=3)

pin_uA=ipin/100.0
iic_nA=iic/100.0

# E=12.3984 keV 
# 2.72924+09 photons/1uA
photon_flux=2.72924E9*pin_uA

print "IC=%7.1f nA PIN=%8.2f uA %8.2e phs/sec"%(iic_nA,pin_uA,photon_flux)
