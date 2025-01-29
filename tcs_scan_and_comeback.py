#!/bin/env python 
import sys
import socket
import time

# My library
from Received import *
from File import *
from TCS import *
import Device

while True:
    #host = '192.168.163.1'
    host = '172.24.242.41'
    port = 10101

    dev=Device.Device(host)
    dev.init()

    # Initialization
    f=File("./")

# Counter channel
    cnt_ch1=0 #0
    cnt_ch2=3 #1

# TCS scan parameters
    scan_apert=0.05
    scan_another_apert=0.5
    scan_start=1.4
    scan_end=2.2
    scan_step=0.05
    scan_time=0.2

# Energy 
    energy=12.3984

# Energy change
    dev.mono.changeE(energy)

# Gap 
    dev.id.moveE(energy)

# Dtheta1 tune
    prefix="%03d"%f.getNewIdx3() ##101025 hashi
    dev.mono.scanDt1PeakConfig(prefix,"DTSCAN_FULLOPEN",dev.tcs)

# Current intensity at 0.1mm sq
    dev.tcs.setApert(0.1,0.1)
    ic_before=dev.countOneSec(0)

# Save current position
    o_vert,o_hori=dev.tcs.getPosition()

# TCS vertical scan
    prefix="%03d"%f.getNewIdx3()
    prefix="%03d_tcs"%f.getNewIdx3()
    tmp,vcenter1=dev.tcs.scanVrel(prefix,0.05,0.50,1.5,scan_step,cnt_ch1,cnt_ch2,scan_time)
    tmp,hcenter1=dev.tcs.scanHrel(prefix,0.50,0.05,1.5,scan_step,cnt_ch1,cnt_ch2,scan_time)
    dev.tcs.setApert(0.1,0.1)
    ic_after=dev.countOneSec(0)

    diffv=vcenter1-o_vert
    diffh=hcenter1-o_hori

    ofile=open("%s_summary.dat"%prefix,"w")
    ofile.write("Original position(V,H)= %8.5f %8.5f\n"%(o_vert,o_hori))
    ofile.write("Tuned    position(V,H)= %8.5f %8.5f\n"%(vcenter1,hcenter1))
    ofile.write("Diff.    position(V,H)= %8.5f %8.5f\n"%(diffv,diffh))
    ofile.write("INT .    before/after = %8d %8d\n"%(ic_before,ic_after))

# Move to the original position
    dev.tcs.setPosition(o_vert,o_hori)

    s.close()
    break
