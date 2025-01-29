#!/bin/env python 
import sys
import socket
import time
import datetime

# My library
from Received import *
from Organizer import *
from ID import *
from Mono import *
from FES import *
from File import *
from TCS import *
from AxesInfo import *
from Stage import *
from Shutter import *
from ExSlit1 import *
from Light import *
from Colli import *
from Gonio import *
from Att import *
from Capture import *
from BM import *
from BS import *
from Cryo import *


while True:
    host = '172.24.242.41'
    port = 10101
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host,port))

    # Initialization
    id=ID(s)
    mono=Mono(s)
    fes=FES(s)
    tcs=TCS(s)
    f=File("./")
    axes=AxesInfo(s)

    stage=Stage(s)
    slit1=ExSlit1(s)
    shutter=Shutter(s)
    light=Light(s)
    gonio=Gonio(s)
    colli=Colli(s)
    att=Att(s)

    cap=Capture()
    moni=BM(s)
    bs=BS(s)
    cryo=Cryo(s)

    dire=os.getcwd()

# Counter channel
    cnt_ch1=0 #0
    cnt_ch2=3 #1

# TCS scan parameters
    scan_apert=0.05
    scan_another_apert=0.5
    scan_start=0.5
    scan_end=1.0
    scan_step=0.05
    scan_time=0.2

# TCS reference value (scan at 12.3984keV, TCS=FO)
    tcs_sh=0.143
    tcs_sv=-0.6210

    hcenter=tcs_sh
    vcenter=tcs_sv


##  Flag for Needle Capture
    NeedleCap_Flag= 1 # Do not Capture
#    NeedleCap_Flag = 1 # will Capture
    #Gonio Posision for Needle
    gny = -12.6847

##  Flag for BeamMonitor Capture
    BMCap_Flag= 1 # Do not Capture
#    BMCap_Flag = 1 # will Capture

    # pixel to micron [um/pixel] in high zoom
    p2u_z=7.1385E-2
    p2u_y=9.770E-2

##  Flag for Stage Tune
    Stage_Flag = 0 # Do not scan
#    Stage_Flag = 1 # will scan

##      Gonio set position [mm] 500um offset from cross point
    sx=-0.1262
    sy=-13.5399
    sz=-0.4734

##      Gonio position for Stage-Z Scan [mm]
    szx=-0.1262
    szy=-13.3449
    szz=-0.0724

##      Gonio position for Stage-Y Scan [mm]
    syx=-0.1312
    syy=-13.1389
    syz=-0.2733

# Output file
    prefix="%03d_StagetTable.dat"%f.getNewIdx3() 
    ofile=open(prefix,"w")
    #ofile.write("time, energy, wait time, dtheta, tcs-vcenter, tcs-hcenter, stz, sty, colli-z, colli-y, pin-count, trans\n")
    ofile.write("time, energy, dtheta, tcs-vcenter, tcs-hcenter, stz, sty, colli-z, colli-y, pin-count, trans\n")
    ofile.flush()

# Energy 
    en_list=[12.3984]
    #en_list=[12.3984,8.5]
    #en_list=[18.0,15.5,12.3984,10.5,8.5]
    #en_list=[8.5,9.5,10.5,12.3984,15.5,18.0]
    #en_list=arange(20.1,8.5,-0.4)


# Wait Time
    #wait_list=[300.0,600.0,900.0,1800.0]
    #wait_list=[3.0,6.0,9.0,18.0]

#    shutter.close()
#    slit1.closeV()
#    colli.goOff()

    for p in arange(0,14,1): # 12hr : 17times
#    for p in arange(0,2,1):
	for en in en_list:
	   # Gap 
	   id.moveE(en)
	   # Energy change
	   mono.changeE(en)
	   wl = 12.3984 / en
	   best_att = att.setAttTrans(wl,0.15)
	   print "Energy: %5.2f keV, Wavelenght: %5.2f A, Attenuator: %s mm\n" % (en, wl, best_att)

	   if en > 20.0:
		print "\nNow waiting!!\n"
		time.sleep(3600)

	   i=0
#	   while i < 2:
	   while i < 1:
	        # Dtheta1 tune
                prefix="%03d_%05.2f"%(f.getNewIdx3(),en)
        
	        # Energy check
		print "dtheata scan\n"
                if en < 10.0:
		    if i == 0:
			tcs.setPosition(vcenter, hcenter)
			mono.scanDt1PeakConfig(prefix,"DTSCAN_LOWE_FO",tcs)
		    else:
			hcenter=tcs_sh
			vcenter=tcs_sv
			tcs.setPosition(vcenter, hcenter)
			mono.scanDt1PeakConfig(prefix,"DTSCAN_LOWENERGY",tcs)
                else:
		    if i == 0:
			tcs.setPosition(vcenter, hcenter)
			mono.scanDt1PeakConfig(prefix,"DTSCAN_FULLOPEN",tcs)
		    else:
			hcenter=tcs_sh
			vcenter=tcs_sv
			tcs.setPosition(vcenter, hcenter)
			mono.scanDt1PeakConfig(prefix,"DTSCAN_NORMAL",tcs)
        
		if i == 0:
			# TCS vertical scan
			prefix="%03d_%05.2f"%(f.getNewIdx3(),en)
			print "\nTCS-V scan\n"
			tmp,vcenter=tcs.scanVrel(prefix,0.05,0.5,1.4,scan_step,cnt_ch1,cnt_ch2,scan_time)
			print "\nTCS-H scan\n"
			tmp,hcenter=tcs.scanHrel(prefix,0.50,0.05,1.4,scan_step,cnt_ch1,cnt_ch2,scan_time)
			tcs.setApert(0.1,0.1)

		if Stage_Flag == 1:
			## Stage Scan
                	gonio.moveXYZmm(sx,sy,sz)
			gonio.moveXYZmm(szx,szy,szz)
			light.off()
			slit1.openV()
			print "\nshutter open\n"
			shutter.open()
			prefix="%03d_%05.2f"%(f.getNewIdx3(),en)
			print "\nStage-Z scan"
			tmp,stz=stage.scanZneedleMove(prefix,0.002,50,3,0,0.2)
			print "\nStage-Y scan"
			gonio.moveXYZmm(sx,sy,sz)
			gonio.moveXYZmm(syx,syy,syz)
			tmp,sty=stage.scanYwire(prefix,0.002,50,3,0,0.2)

			## Collimator scan
			## evacuation of a wire
			print "\nColli scan\n"
			gonio.moveXYZmm(sx,sy,sz)
			prefix="%03d_%05.2f"%(f.getNewIdx3(),en)
			colli_y,colli_z=colli.scan(prefix,3) #PIN after sample position
			att.att0um()
			trans,pin=colli.compareOnOff(3)
			att.setAtt(best_att)
			shutter.close()
			slit1.closeV()
			colli.goOff()
		else:
			colli_y = 0
			colli_z = 0
			sty = 0
			stz = 0
			trans = 0
			pin = 0

		if NeedleCap_Flag == 1:
                        print "Needle Cap\n"
                        print "bm off\n"
                        moni.offXYZ()
                        print "Move Gonio\n"
                        gonio.moveYmm(gny)
                        print "light on\n"
                        light.on()

                        print "capture\n"
                        prefix="%03d_%05.2f"%(f.getNewIdx3(),en)
                        filename="%s/%s_Needle_Cap.ppm"%(dire,prefix)
                        cap.capture(filename,52)

                        print "light off\n"
                        light.off()

		if BMCap_Flag == 1:
                        print "BM Cap\n"
                        print "Gonio Move\n"
                        gonio.moveYmm(gny + 10.0)
                        att.setAttTrans(wl,0.03)
                        print "Energy: %5.2f keV, Wavelenght: %5.2f A, Attenuator: %s mm\n" % (en, wl, best_att)

                        print "light off\n"
                        light.off()
                        print "cryo off\n"
                        cryo.off()
                        print "bs on\n"
                        bs.on()
                        print "bm on\n"
                        moni.onPika()
                        print "slit1 open\n"
                        slit1.openV()
                        print "shutter open\n"
                        shutter.open()

                        print "\n capture\n"
                        prefix="%03d_%05.2f"%(f.getNewIdx3(),en)
                        filename="%s/%s_BM_Cap.ppm"%(dire,prefix)
                        x,y=cap.captureBM(filename,22)
                        sty=x*p2u_y
                        stz=y*p2u_z

                        print "shutter close\n"
                        shutter.close()
                        print "slit1 close\n"
                        slit1.closeV()
                        print "bm off\n"
                        moni.offXYZ()
                        print "bs off\n"
                        bs.off()
                        print "cryo on\n"
                        cryo.on()
                        att.setAtt(best_att)
                        print "Gonio Move\n"
                        gonio.moveYmm(gny)

                dt1=mono.getDt1()
                dtime=datetime.datetime.now()

		# Save current axes information
                #ofile.write("%20s, %9.4f, %10.1f, %10d, %8.4f, %8.4f, %8.4f, %8.4f, %8.4f, %8.4f, %5.2f, %5.2f\n"%(dtime,en,wait_time,dt1,vcenter,hcenter,stz,sty,colli_z,colli_y,pin,trans))
                ofile.write("%20s, %9.4f, %10d, %8.4f, %8.4f, %8.4f, %8.4f, %8.4f, %8.4f, %5.2f, %5.2f\n"%(dtime,en,dt1,vcenter,hcenter,stz,sty,colli_z,colli_y,pin,trans))
                ofile.flush()
		i += 1

	   print "\nNow waiting!!\n"
	   time.sleep(1800)

    ofile.close()
    id.moveE(12.3984)
    mono.changeE(12.3984)

    s.close()
    break
