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


    infolist=[]

# Counter channel
    cnt_ch1=0 #110117 IC  before Mirror
    cnt_ch2=3 #110117 PIN before Mirror

# FES scan setting
    scan_apert=0.05
    scan_another_apert=0.5
    scan_start=-1.5
    scan_end=2.0
    scan_step=0.05
    scan_time=0.2

# Energy change to 23.2keV
    mono.changeE(23.2)
    #mono.changeE(12.3984)
# Gap full open
    id.move(44.999) # Full open
    #id.move(10.041) # Full open

# FES open
    fes.setApert(0.3,0.3)

# Dtheta1 tune

    prefix="%03d"%f.getNewIdx3() ## 100629 hashi

    try :
            ## Dtheta 1
            scan_dt1_ch1=int(conf.getCondition2("DTSCAN_FULLOPEN","ch1"))
            scan_dt1_ch2=int(conf.getCondition2("DTSCAN_FULLOPEN","ch2"))
            scan_dt1_start=int(conf.getCondition2("DTSCAN_FULLOPEN","start"))
            scan_dt1_end=int(conf.getCondition2("DTSCAN_FULLOPEN","end"))
            scan_dt1_step=int(conf.getCondition2("DTSCAN_FULLOPEN","step"))
            scan_dt1_time=conf.getCondition2("DTSCAN_FULLOPEN","time")
            tcsv=conf.getCondition2("DTSCAN_FULLOPEN","tcsv")
            tcsh=conf.getCondition2("DTSCAN_FULLOPEN","tcsh")

    except MyException,ttt:
            print ttt.args[0]
            print "Check your config file carefully.\n"
            sys.exit(1)

    tcs.setApert(tcsv,tcsh)
    mono.scanDt1Peak(prefix,scan_dt1_start,scan_dt1_end,scan_dt1_step,scan_dt1_ch1,scan_dt1_ch2,scan_dt1_time)

# Counter channel
    cnt_ch1=3 #171122 Pin  before Mirror
    cnt_ch2=0 #171122 IC  before Mirror

# FES vertical scan
    prefix="%03d"%f.getNewIdx3()
    fes.scanBoth(prefix,scan_apert,scan_another_apert,scan_start,scan_end,scan_step,cnt_ch1,cnt_ch2,scan_time)

# FES Apearture set
    fes.setApert(0.34,0.30)

# Save current axes information
    prefix="%03d"%f.getNewIdx3()
    ofile=prefix+"_axes.dat"
    axes.all(ofile)

    s.close()
    break
