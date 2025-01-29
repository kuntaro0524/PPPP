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

# Output file
    ofile=open("energy_wait.dat","w")
    ofile.write("time, energy, wait time, dtheta, vcenter, hcenter\n")
    ofile.flush()

# Energy 
    #en_list=[12.3984,8.5]
    enlist=[12.3984,18.0,15.5,10.5,8.5]
    wait_list=[300.0,600.0,900.0,1800.0]
    #wait_list=[3.0,6.0,9.0,18.0]

    for p in arange(0,20,1):
        for en in en_list:
            # Energy change
            mono.changeE(en)
            # Gap 
            id.moveE(en)
    
            for wait_time in wait_list:
	        # Dtheta1 tune
                prefix="%03d"%f.getNewIdx3() 
        
	        # Energy check
                if en < 10.0:
                    mono.scanDt1PeakConfig(prefix,"DTSCAN_LOWENERGY",tcs)
                else:
                    mono.scanDt1PeakConfig(prefix,"DTSCAN_FULLOPEN",tcs)
        
	        # TCS vertical scan
                prefix="%03d"%f.getNewIdx3()
                prefix="%03d_tcs"%f.getNewIdx3()
                tmp,vcenter1=tcs.scanVrel(prefix,0.05,0.5,1.4,scan_step,cnt_ch1,cnt_ch2,scan_time)
                tmp,hcenter1=tcs.scanHrel(prefix,0.50,0.05,1.4,scan_step,cnt_ch1,cnt_ch2,scan_time)
    
                dt1=mono.getDt1()
                dtime=datetime.datetime.now()
    
                ofile.write("%20s, %9.4f, %10.1f, %10d, %8.4f, %8.4f\n"%(dtime,en,wait_time,dt1,vcenter1,hcenter1))
                ofile.flush()
                print "Waiting for %10.1f seconds..."%wait_time
                time.sleep(wait_time)
	
# Save current axes information
    ofile.close()
    s.close()
    break
