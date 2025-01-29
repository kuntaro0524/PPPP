import sys
import socket
import time
import datetime
import math
import timeit

sys.path.append("/isilon/BL32XU/BLsoft/PPPP")
import File
from pylab import *

# My library
import Device

if __name__=="__main__":
    dev=Device.Device("172.24.242.41")
    dev.init()

##  Device definition
    f=File.File("./")

    ofile="%03d_count.scn"%(f.getNewIdx3())
    fff=open(ofile,"w")

    dev.mono.changeE(12.3984)
    prefix="%03d_dtscan"%(f.getNewIdx3())
    fwhm,center=dev.mono.scanDt1PeakConfig(prefix,"DTSCAN_NORMAL",dev.tcs)

    print "prepscan"
    dev.prepScan()
    print "colli off pos"
    dev.colli.off()

    fff.write("time, Comment, IC (nA), Pin (uA), dt1\n")
    ti=datetime.datetime.now()
    ipin,iic=dev.countPin(3)
    pin_uA=ipin/100.0
    iic_nA=iic/100.0
    fff.write("%20s, init at 12.3984 keV, %5.2f, %5.2f, %8d\n"%(ti,iic_nA,pin_uA,center))
    fff.flush()

    print "Shutter close"
    dev.shutter.close()
    print "Ex1 slit moves to close position"
    dev.slit1.closeV()


    idx=0
    while(1):
        print "mono move to 17.0 keV"
        dev.mono.changeE(17.0)
        print "mono move to 12.3984 keV"
        dev.mono.changeE(12.3984)
        prefix="%03d_dtscan"%(f.getNewIdx3())
        fwhm,center=dev.mono.scanDt1PeakConfig(prefix,"DTSCAN_NORMAL",dev.tcs)

        # Prep scan
        print "Ex1 slit moves to open position"
        dev.slit1.openV()
        print "Shutter open"
        dev.shutter.open()

        #dev.countPin(3)
        ti=datetime.datetime.now()
        pin_uA=ipin/100.0
        iic_nA=iic/100.0
        fff.write("%20s, from 17.0 keV, %5.2f, %5.2f, %8d\n"%(ti,iic_nA,pin_uA,center))
        fff.flush()

        print "Shutter close"
        dev.shutter.close()
        print "Ex1 slit moves to close position"
        dev.slit1.closeV()

        print "mono move to 9.0 keV"
        dev.mono.changeE(9.0)
        print "mono move to 12.3984 keV"
        dev.mono.changeE(12.3984)
        prefix="%03d_dtscan"%(f.getNewIdx3())
        fwhm,center=dev.mono.scanDt1PeakConfig(prefix,"DTSCAN_NORMAL",dev.tcs)

        # Prep scan
        print "Ex1 slit moves to open position"
        dev.slit1.openV()
        print "Shutter open"
        dev.shutter.open()

        ti=datetime.datetime.now()
        #dev.countPin(3)

        ipin,iic=dev.countPin(3)
        pin_uA=ipin/100.0
        iic_nA=iic/100.0
        fff.write("%20s, from 9.0keV, %5.2f, %5.2f, %8d\n"%(ti,iic_nA,pin_uA,center))
        fff.flush()

        print "Shutter close"
        dev.shutter.close()
        print "Ex1 slit moves to close position"
        dev.slit1.closeV()

        idx+=1

        if idx>10:
            break

    fff.close()
    dev.shutter.close()
    dev.slit1.closeV()
    dev.mono.changeE(12.3984)
    s.close()
