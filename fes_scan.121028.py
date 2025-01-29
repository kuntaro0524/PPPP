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
    scan_end=2.5
    scan_step=0.05
    scan_time=0.2

# Gap full open
    id.move(10.063) 

# Energy List
#    enlist=[12.3984,11.96,12.295,12.415,12.475,12.515,12.63,12.68,12.72]
    enlist=[12.3984]
    fesv=0.51550
    fesh=0.47100
    fes.fes_vert.move(fesv)
    fes.fes_hori.move(fesh)

    prefix="%03d"%f.getNewIdx3()
    ofile=prefix+"_axes.dat"
    axes.all(ofile)

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

    for en in enlist:
	prepre = "e%07.3f"%en

# FES open
	fes.setApert(0.3,0.3)

# Energy change
	mono.changeE(en)

##	time.sleep(600)

# Dtheta1 tune
	prefix="%03d_%s"%(f.getNewIdx3(),prepre)
	mono.scanDt1Peak(prefix,scan_dt1_start,scan_dt1_end,scan_dt1_step,scan_dt1_ch1,scan_dt1_ch2,scan_dt1_time)

# FES Both scan
	prefix="%03d_%s"%(f.getNewIdx3(),prepre)
#	fes.scanBothNoAnal(prefix,scan_apert,scan_another_apert,scan_start,scan_end,scan_step,cnt_ch1,cnt_ch2,scan_time)
	fes.scanBoth(prefix,scan_apert,scan_another_apert,scan_start,scan_end,scan_step,cnt_ch1,cnt_ch2,scan_time)
	prefix="%03d_%s"%(f.getNewIdx3(),prepre)
	fes.scanBoth(prefix,scan_apert,scan_another_apert,scan_start,scan_end,scan_step,cnt_ch1,cnt_ch2,scan_time)

# FES open
	fes.setApert(0.3,0.3)

# Save current axes information
	prefix="%03d_%s"%(f.getNewIdx3(),prepre)
	ofile=prefix+"_axes.dat"
	axes.all(ofile)

    s.close()
    break
