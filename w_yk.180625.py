#!/bin/env python import sys import socket
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

##    Device definition
    f=File.File("./")

    scan_yaxis = "true"
    scan_zaxis = "true"

##      TCS aperture list
        #tcs_list=[(0.5,0.5),(0.026,0.040),(0.1,0.1),(0.2,0.2),(0.3,0.3),(1.0,0.04)]
    #tcs_list=[(3.0,3.0),(0.1,0.1),(0.411,0.346)]
    tcs_list=[(0.5,0.5),(0.1,0.1),(0.026,0.040)]
    #tcs_list=[(3.0,3.0)]

#        tcs_list=[(0.5,0.5),(0.026,0.040)]

    #prepre="g%s"%scan_axis
    prepre="tcs"

    en=12.3984

############################

    def_gx=1.6329
    def_gy=-11.4610
    def_gz=-1.5760

############################
    sy_gy=-11.3110
    sz_gz=-1.4260

#    sx,sy,sz=dev.gonio.getXYZmm()

#    xp=sx*1000.0
#    yp=sy*1000.0
#    zp=sz*1000.0

#    print "Current Gonio Positon (um): %10.3f,%10.3f, %10.3f"%(xp,yp,zp)

##     Prep scan
    dev.prepScan()
    dev.colli.off()

##     Log file
    logname="%03d_wire.log"%(f.getNewIdx3())
    logf=open(logname,"w")

##    Counter channel
    cnt_ch1=3
    cnt_ch2=0

    ## Collimator scan
    ## evacuation of a wire
    dev.gonio.moveXYZmm(def_gx,def_gy,def_gz)

#    prefix="%03d_colli"%(f.getNewIdx3())
#    colli_y,colli_z=dev.colli.scan(prefix,3) #PIN after sample position
#    cntstr_colli=dev.countPin(3)
#    trans,pin=dev.colli.compareOnOff(3)


##     Wire scan

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
            nstep_y=30 # 
        elif tcsh < 1.0:
            gstep_y=0.5
            ssec_y=0.2
            nstep_y=50 # 
        else :
            gstep_y=0.5
            ssec_y=0.5
            nstep_y=250 # 
    
        # Check TCS aperture Vertical
        if tcsv < 0.07:
            gstep_z=0.1
            ssec_z=0.5
            nstep_z=100 # 
        elif tcsv < 0.26:
            gstep_z=0.2
            ssec_z=0.2
            nstep_z=50 # 
        elif tcsv < 1.0:
            gstep_z=0.5
            ssec_z=0.2
            nstep_z=50 # 
        else :
            gstep_z=0.5
            ssec_z=0.5
            nstep_z=250 # 

        ywidth=0
        zwidth=0
        ycenter=0
        zcenter=0
    
#scan_axis == "y":
        if scan_yaxis == "true":

            tmp=def_gy-0.1
            yp=sy_gy*1000.0

            dev.gonio.moveXYZmm(def_gx,tmp,def_gz)

            # photon flux
            ipin,iic=dev.countPin(3)
            pin_uA=ipin/100.0
            iic_nA=iic/100.0
            cntstr="%s"%ipin
            flux=dev.calcFlux(en,pin_uA)

            # range
            ystart=yp-float(nstep_y)*gstep_y
            yend=yp+float(nstep_y)*gstep_y
            print "Scan Y range: %10.3f - %10.3f\n"%(ystart,yend)
            ywidth,ycenter=dev.gonio.scanYenc(prefix,ystart,yend,gstep_y,cnt_ch1,cnt_ch2,ssec_y)

        if scan_zaxis == "true":
#        scan_axis == "z":

            tmp=sz_gz-0.1
            zp=sz_gz*1000.0

            dev.gonio.moveXYZmm(def_gx,def_gy,tmp)

        # photon flux
            ipin,iic=dev.countPin(3)
            pin_uA=ipin/100.0
            iic_nA=iic/100.0
            cntstr="%s"%ipin
            flux=dev.calcFlux(en,pin_uA)

        # range
            zstart=zp-float(nstep_z)*gstep_z
            zend=zp+float(nstep_z)*gstep_z
            print "Scan Z range: %10.3f - %10.3f\n"%(zstart,zend)
            zwidth,zcenter=dev.gonio.scanZenc(prefix,zstart,zend,gstep_z,cnt_ch1,cnt_ch2,ssec_z)

        logf.write("%5.3f x %5.3f (v x h),  %8.3f um %8.3f pls %8.3f um %8.3f pls ( Pin Vlaue: %5.2e uA Flux: %5.2e  )\n"%(tcsv,tcsh,zwidth,zcenter,ywidth,ycenter,pin_uA,flux))
        print("\n\n%5.3f x %5.3f (v x h),  %8.3f um %8.3f pls %8.3f um %8.3f pls ( Pin Vlaue: %5.2e uA Flux: %5.2e  )\n"%(tcsv,tcsh,zwidth,zcenter,ywidth,ycenter,pin_uA,flux))


    # Move wire to default position
    dev.gonio.moveXYZmm(def_gx,def_gy,def_gz)

    logf.flush()

    # Finishing scan before the next delta_theta1 tune
#    print "Scan finished! Ex1 slit moves to close position"
#    dev.slit1.closeV()
    print "Scan finished! Shutter moves to close position"
    #dev.shutter.close()
    dev.closeAllShutter()

    dev.colli.off()

    logf.close()

    break
