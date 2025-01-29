#!/bin/env python import sys import socket
import time,os,math,sys
import math

sys.path.append("/isilon/BL32XU/BLsoft/PPPP")
import File
from pylab import *

# My library
import Device

def_gx=-1.5409
def_gy=-11.3672
def_gz=-0.8074

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
    dthetaTuneFlag=True
    #dthetaTuneFlag=False

#   Collimaeter tune Flag
    #ColliScanFlag=True
    ColliScanFlag=False

##      TCS aperture list (V x H)
    #tcs_list=[(0.026,0.040),(0.05,0.05),(0.1,0.1),(0.2,0.2),(0.3,0.3),(0.4,0.4),(0.5,0.5),(1.0,0.04)]
    tcs_list=[(0.5,0.5),(0.026,0.040)]
    #tcs_list=[(0.026,0.040)]

    #prepre="g%s"%scan_axis
    prepre="tcs"

    en=12.3984

############################
##  Gonio set position [mm]

    def_gx,def_gy,def_gz=dev.gonio.getXYZmm()
    print def_gx,def_gy,def_gz
    #def_gx=-1.5409
    #def_gy=-11.3672
    #def_gz=-0.8074

##  Beam Center position [mm]

    #sy_gy= -11.2182
    #sz_gz=-0.6494
    if scan_yaxis and scan_zaxis:
        print "scan both axis"
        sy_gy= def_gy + 0.150
        sz_gz= def_gz + 0.150
    elif scan_zaxis == False:
        print "scan only y-axis"
        sy_gy= def_gy
        def_gy= sy_gy - 0.150
    elif scan_yaxis == False:
        print "scan only z-axis"
        sz_gz= def_gz
        def_gz= sz_gz - 0.150

    #break

    #print "sleep 60 sec\n"
    #time.seep(60)

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
       #dev.colli.on()
       print "skip colli-scan"

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
            gstep_y=0.2
            ssec_y=0.2
            nstep_y=50 # 
        elif tcsh > 0.3:
            gstep_y=0.5
            ssec_y=0.2
            nstep_y=50 # 
        else :
            gstep_y=0.3
            ssec_y=0.2
            nstep_y=50 # 
    
        # Check TCS aperture Vertical
        if tcsv < 0.1:
            gstep_z=0.2
            ssec_z=0.2
            nstep_z=50 # 
        elif tcsv > 0.3:
            gstep_z=0.5
            ssec_z=0.2
            nstep_z=50 # 
        else :
            gstep_z=0.3
            ssec_z=0.2
            nstep_z=50 # 

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
#            sy_gy=float(ycenter)/1000.0
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
#            sz_gz=float(zcenter)/1000.0
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
    dev.finishScan()
    #dev.closeAllShutter()
    dev.gonio.moveXYZmm(def_gx,def_gy,def_gz)
    dev.colli.off()

    logf.close()

    break
