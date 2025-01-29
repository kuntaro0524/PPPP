#!/bin/env python 
import sys
import socket
import time

# My library
from Received import *
from Organizer import *
from ID import *
from Mono import *
from FES import *
from File import *
from TCS import *
from AxesInfo import *
from ConfigFile import *

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
    conf=ConfigFile()


    print 'File prefix ='

    infolist=[]

# Counter channel
    cnt_ch1=0 #100605 IC  before Mirror
    cnt_ch2=3 #100605 PIN before Mirror

# FES scan setting
    scan_apert=0.05
    scan_another_apert=0.5
    scan_start=-1.5
    scan_end=2.0
    scan_step=0.05
    scan_time=0.2

# Dtheta1 tune range
    try :
            ## Dtheta 1
            scan_dt1_ch1=int(conf.getCondition2("DTSCAN_NORMAL","ch1"))
            scan_dt1_ch2=int(conf.getCondition2("DTSCAN_NORMAL","ch2"))
            scan_dt1_start=int(conf.getCondition2("DTSCAN_NORMAL","start"))
            scan_dt1_end=int(conf.getCondition2("DTSCAN_NORMAL","end"))
            scan_dt1_step=int(conf.getCondition2("DTSCAN_NORMAL","step"))
            scan_dt1_time=conf.getCondition2("DTSCAN_NORMAL","time")
            tcsv=conf.getCondition2("DTSCAN_NORMAL","tcsv")
            tcsh=conf.getCondition2("DTSCAN_NORMAL","tcsh")

    except MyException,ttt:
            print ttt.args[0]
            print "Check your config file carefully.\n"
            sys.exit(1)

# Energy change to 23.2keV
    #mono.changeE(23.2)
# Gap full open
    #id.move(45.0) # Full open

# Height offset 140405 0.044mm
    height_offset=0.044

# FES open
    #fes.setApert(0.3,0.3)
# TCS full open
    #tcs.setApert(3.0,3.0)
# Dtheta1 tune
    #prefix="%03d"%f.getNewIdx3() ## 100629 hashi
    #mono.scanDt1Peak(prefix,scan_dt1_start,scan_dt1_end,scan_dt1_step,scan_dt1_ch1,scan_dt1_ch2,scan_dt1_time)  #hashi 100628

# FES vertical scan
    prefix="%03d"%f.getNewIdx3()
    fes.scanH(prefix,scan_another_apert+height_offset,scan_apert,scan_start,scan_end,scan_step,cnt_ch1,cnt_ch2,scan_time)

# Save current axes information
    prefix="%03d"%f.getNewIdx3()
    ofile=prefix+"_axes.dat"
    axes.all(ofile)

    s.close()
    break
