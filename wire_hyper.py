#!/bin/env python import sys import socket
import time, os, math, sys
import math

sys.path.append("/isilon/BL32XU/BLsoft/PPPP")
import File
from pylab import *

# My library
import Device


##	Usefull function
def wire_rough_scan(sx, sy, sz):  # sx,sy,sz = wire default
    ## Wire rough scan
    ssz = sz + 0.1
    dev.gonio.moveXYZmm(sx, sy, ssz)
    xp, zp = dev.gonio.wireRoughZ(3)
    ssy = sy + 0.1
    dev.gonio.moveXYZmm(sx, ssy, sz)
    yp = dev.gonio.wireRoughY(3)

    # mm -> um
    xp = xp * 1000.0
    yp = yp * 1000.0
    zp = zp * 1000.0
    print "##### Wire Rough %8.5f %8.5f %8.5f\n" % (xp, yp, zp)

    return xp, yp, zp


while True:
    dev = Device.Device("172.24.242.41")
    dev.init()

    ##	Device definition
    f = File.File("./")

    ## 	Gonio set position [mm]
    sx = 0.8829
    sy = -11.4584
    sz = -0.8647

    ## 	Prep scan
    dev.prepScan()

    print "Ex1 slit moves to close position"
    dev.slit1.closeV()
    print "Shutter close"
    dev.shutter.close()

    ## 	Energy list
    enlist = [12.3984]

    ## 	TCS aperture list
    # Itsumono
    # Normally used TCS aperture (V, H)
    tcs_list = [(0.5, 0.04)]

    ## 	Log file
    logname = "%03d_wire.log" % (f.getNewIdx3())
    logf = open(logname, "w")

    ##	Counter channel
    cnt_ch1 = 3
    cnt_ch2 = 0

    #	Dtheta tune
    # dthetaTuneFlag=True
    dthetaTuneFlag = False

    ## 	Wire scan
    for en in enlist:
        # Energy change
        dev.mono.changeE(en)
        dev.id.moveE(en)
        # time.sleep(900)
        # Prefix of prefix
        prepre = "e%07.3f" % en

        if dthetaTuneFlag:
            prefix = "%03d_%s" % (f.getNewIdx3(), prepre)
            dev.mono.scanDt1PeakConfig(prefix, "DTSCAN_NORMAL", dev.tcs)

        # Prep scan
        print "Ex1 slit moves to open position"
        dev.slit1.openV()
        print "Shutter open"
        dev.shutter.open()

        ## Collimator scan
        ## evacuation of a wire
        dev.gonio.moveXYZmm(sx, sy, sz)
        prefix = "%03d_colli" % (f.getNewIdx3())
        colli_y, colli_z = dev.colli.scan(prefix, 3)  # PIN after sample position
        cntstr_colli = dev.countPin(3)
        trans, pin = dev.colli.compareOnOff(3)

        for tcs_param in tcs_list:
            # Prep scan (All shutter is closed when the wire scan finished)
            # They should be opened here for loop experiments
            print "Ex1 slit moves to open position"
            dev.slit1.openV()
            print "Shutter open"
            dev.shutter.open()

            # TCS aparture
            tcsv = float(tcs_param[0])
            tcsh = float(tcs_param[1])

            # TCS set aperture
            dev.tcs.setApert(tcsv, tcsh)

            # TCS str
            tcsstr = "%4.3fx%4.3f" % (tcsv, tcsh)

            # PREFIX
            prefix = "%03d_%s_%s" % (f.getNewIdx3(), prepre, tcsstr)

            # Check TCS aperture Horizontal
            if tcsh < 0.1:
                gstep_y = 0.1
                ssec_y = 2.0
                nstep_y = 100  #
            elif tcsh < 0.4:
                gstep_y = 0.5
                ssec_y = 2.0
                nstep_y = 30  #
            else:
                gstep_y = 1.0
                ssec_y = 2.0
                nstep_y = 20  #

            # Check TCS aperture Vertical
            if tcsv < 0.07:
                gstep_z = 0.1
                ssec_z = 2.0
                nstep_z = 100  #
            elif tcsv < 0.26:
                gstep_z = 0.2
                ssec_z = 2.0
                nstep_z = 50  #
            elif tcsv < 5.0:
                gstep_z = 0.5
                ssec_z = 2.0
                nstep_z = 50  #

            # Move wire to default position
            dev.gonio.moveXYZmm(sx, sy, sz)
            # Wire rough scan
            xp, yp, zp = wire_rough_scan(sx, sy, sz)  # sx,sy,sz = wire default
            print "Wire rough position: %10.2f %10.2f %10.2f [um]" % (xp, yp, zp)

            # range
            ystart = yp - float(nstep_y) * gstep_y
            yend = yp + float(nstep_y) * gstep_y
            zstart = zp - float(nstep_z) * gstep_z
            zend = zp + float(nstep_z) * gstep_z
            print "Scan Y range: %10.3f - %10.3f" % (ystart, yend)
            print "Scan Z range: %10.3f - %10.3f" % (zstart, zend)

            # set position
            ywidth, ycenter = dev.gonio.scanYenc(prefix, ystart, yend, gstep_y, cnt_ch1, cnt_ch2, ssec_y)

            dev.gonio.moveXYZmm(sx, sy, sz)
            zwidth, zcenter = dev.gonio.scanZenc(prefix, zstart, zend, gstep_z, cnt_ch1, cnt_ch2, ssec_z)

            # Flux measurements
            # PIN counter
            dev.gonio.moveXYZmm(sx, sy, sz)
            dev.countPin(3)

            # photon flux
            ipin, iic = dev.countPin(3)
            pin_uA = ipin / 100.0
            iic_nA = iic / 100.0

            cntstr = "%s" % ipin
            flux = dev.calcFlux(en, pin_uA)

            logf.write(
                "%8.4f %5.1f %5.1f %5.3f %5.3f %8.3f %8.3f %8.3f %8.3f %s ( Flux: %5.2e, Trans: %5.2f percent )\n" % (
                en, colli_y, colli_z, tcsv, tcsh, zwidth, zcenter, ywidth, ycenter, cntstr, flux, trans))
            logf.flush()

            # Finishing scan before the next delta_theta1 tune
            print "Scan finished! Ex1 slit moves to close position"
            dev.slit1.closeV()
            print "Scan finished! Shutter moves to close position"
            dev.shutter.close()
    logf.close()
    dev.slit1.closeV()
    dev.id.moveE(12.3984)
    dev.mono.changeE(12.3984)

    break
