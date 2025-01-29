#!/bin/env python import sys import socket
##### For Hyper Focus Mode ##############
import time,os,math,sys
import math

sys.path.append("/isilon/BL32XU/BLsoft/PPPP")
import File
from pylab import *

# My library
import Device

while True:
    dev=Device.Device("172.24.242.41")
    dev.init()

##   Device definition
    f=File.File("./")

#   Scane axis Flag
    scan_yaxis = True
    #scan_yaxis = False
    scan_zaxis = True
    #scan_zaxis =False

#   Dtheta tune Flag
    #dthetaTuneFlag=True
    dthetaTuneFlag=False

#   Collimaeter tune Flag
    ColliScanFlag=True
    #ColliScanFlag=False

##      TCS aperture list
    #tcs_list=[(0.026,0.040),(0.05,0.05),(0.1,0.1),(0.2,0.2),(0.3,0.3),(0.4,0.4),(0.5,0.5),(1.0,0.04)]
    #tcs_list=[(0.5,0.5),(0.026,0.040),(0.5,0.04)]
    #tcs_list=[(0.026,0.040)]

    # For Hyper Focus Mode
    #tcs_list=[(0.5,0.5),(0.5,0.04)]
    tcs_list=[(0.5,0.04)]
    #tcs_list=[(0.5,0.04),(0.5,0.08),(0.5,0.10),(0.5,0.15),(0.5,0.20)]

    #prepre="g%s"%scan_axis
    prepre="tcs"

    en=12.3984

############################
##  Gonio set position [mm]

    def_gx=1.7230
    def_gy=-13.2090
    def_gz=-1.9090

##  Beam Center position [mm]

    sy_gy=-13.0590
    sz_gz=-1.7590

############################

#    sx,sy,sz=dev.gonio.getXYZmm()

#    xp=sx*1000.0
#    yp=sy*1000.0
#    zp=sz*1000.0

#    print "Current Gonio Positon (um): %10.3f,%10.3f, %10.3f"%(xp,yp,zp)

##     Log file
    logname="%03d_wire.log"%(f.getNewIdx3())
    logf=open(logname,"w")

##    Counter channel
    cnt_ch1=3
    cnt_ch2=0

    ## evacuation of a wire
    dev.gonio.moveXYZmm(def_gx,def_gy,def_gz)

#   Dtheta tune
    if dthetaTuneFlag:
        prefix="%03d_%s"%(f.getNewIdx3(),prepre)
        dev.mono.scanDt1PeakConfig(prefix,"DTSCAN_NORMAL",dev.tcs)

## Prep scan
    dev.prepScan()

## Collimator scan
    if ColliScanFlag:
        prefix="%03d_colli"%(f.getNewIdx3())
        colli_y,colli_z=dev.colli.scan(prefix,3) #PIN after sample position
        cntstr_colli=dev.countPin(3)
        trans,pin=dev.colli.compareOnOff(3)
    else :
       dev.colli.on()

##     Wire scan
    i = 0
    for tcs_param in tcs_list:

        # TCS aparture
        tcsv=float(tcs_param[0])
        tcsh=float(tcs_param[1])

        # TCS set aperture
        dev.tcs.setApert(tcsv,tcsh)
    
        # TCS str
        tcsstr="%4.3fx%4.3f"%(tcsv,tcsh)
    
        # PREFIX
        prefix="%03d_%s_%s"%(f.getNewIdx3(),prepre,tcsstr)

        # Check TCS aperture Horizontal
        if tcsh < 0.1:
            gstep_y=0.1
            ssec_y=0.5
            nstep_y=100 # 
        elif tcsh < 0.4:
            gstep_y=0.5
            ssec_y=0.2
            nstep_y=30
        elif tcsh < 1.0:
            gstep_y=0.5
            ssec_y=0.2
            nstep_y=50
        else :
            gstep_y=0.5
            ssec_y=0.5
            nstep_y=250
    
        # Check TCS aperture Vertical 
        if tcsv < 0.07:
            gstep_z=0.1
            ssec_z=0.5
            nstep_z=100
        elif tcsv < 0.26:
            gstep_z=0.2
            ssec_z=0.2
            nstep_z=50
        elif tcsv < 1.0:
            gstep_z=0.5
            ssec_z=0.2
            nstep_z=50
        else :
            gstep_z=0.5
            ssec_z=0.5
            nstep_z=250

        # Check TCS aperture Vertical for HyperFocusMode
        gstep_z=0.1
        ssec_z=0.5
        nstep_z=100

        ywidth=0
        zwidth=0
        ycenter=0
        zcenter=0
    
        dev.gonio.moveXYZmm(def_gx,def_gy,def_gz)

        # photon flux
        ipin,iic=dev.countPin(3)
        pin_uA=ipin/100.0
        iic_nA=iic/100.0
        cntstr="%s"%ipin
        flux=dev.calcFlux(en,pin_uA)

#scan_axis == "y":
        if scan_yaxis:
            yp=sy_gy*1000.0

            # range
            ystart=yp-float(nstep_y)*gstep_y
            yend=yp+float(nstep_y)*gstep_y
            print "Scan Y range: %10.3f - %10.3f\n"%(ystart,yend)
            ywidth,ycenter=dev.gonio.scanYenc(prefix,ystart,yend,gstep_y,cnt_ch1,cnt_ch2,ssec_y)
            sy_gy=float(ycenter)/1000.0
            print "sy_gy =",sy_gy

            # Move wire to default position
            dev.gonio.moveXYZmm(def_gx,def_gy,def_gz)

        if scan_zaxis:
#        scan_axis == "z":
            dev.gonio.moveXYZmm(def_gx,def_gy,def_gz)

            zp=sz_gz*1000.0

        # range
            zstart=zp-float(nstep_z)*gstep_z
            zend=zp+float(nstep_z)*gstep_z
            print "Scan Z range: %10.3f - %10.3f\n"%(zstart,zend)
            zwidth,zcenter=dev.gonio.scanZenc(prefix,zstart,zend,gstep_z,cnt_ch1,cnt_ch2,ssec_z)
            sz_gz=float(zcenter)/1000.0
            print "sz_gz =",sz_gz

 # Move wire to default position
            dev.gonio.moveXYZmm(def_gx,def_gy,def_gz)

        logf.write("%5.3f x %5.3f (v x h),  %8.3f um %8.3f pls %8.3f um %8.3f pls ( IC Value: %5.2e nA, Pin Vlaue: %5.2e uA, Flux: %5.2e  )\n"%(tcsv,tcsh,zwidth,zcenter,ywidth,ycenter,iic_nA,pin_uA,flux))
        print("\n\n%5.3f x %5.3f (v x h),  %8.3f um %8.3f pls %8.3f um %8.3f pls ( IC Value: %5.2e nA, Pin Vlaue: %5.2e uA, Flux: %5.2e  )\n"%(tcsv,tcsh,zwidth,zcenter,ywidth,ycenter,iic_nA,pin_uA,flux))
        #logf.write("%8.4f %5.1f %5.1f %5.3f %5.3f %8.3f %8.3f %8.3f %8.3f %s ( Flux: %5.2e, Trans: %5.2f percent )\n"%(en,colli_y,colli_z,tcsv,tcsh,zwidth,zcenter,ywidth,ycenter,cntstr,flux,trans))

        logf.flush()

    # Finishing scan before the next delta_theta1 tune
#    print "Scan finished! Ex1 slit moves to close position"
#    dev.slit1.closeV()
    print "Scan finished! Shutter moves to close position"
    #dev.finishScan()
    #dev.closeAllShutter()
    dev.colli.off()

    logf.close()

    break
