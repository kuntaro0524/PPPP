#!/bin/env python 
import sys
import socket
import time
import datetime

# My library
from Mono import *
from FES import *
from ID import *
from TCS import *
from ExSlit1 import *
from AxesInfo import *
from File import *

host = '172.24.242.41'
port = 10101
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))

while True:

# St2Slit1 knife edge scan
    slit1_start=18010
    slit1_end=10
    slit1_step=-100
    slit1_ch0=3
    slit1_ch1=0

# Detector number
    cnt_ch1=3
    cnt_ch2=0

# Devices
    mono=Mono(s)
    tcs=TCS(s)
    exs=ExSlit1(s)
    axes=AxesInfo(s)
    f=File("./")

    index=0
    sizei=0

    # Log file
    logf=open("beampos.dat","w")
    prefix="%03d"%f.getNewIdx3()
    exs.fullOpen()

    slit1_vfwhm,slit1_vcenter=exs.scanV(prefix,-slit1_start,-slit1_end,-slit1_step,slit1_ch0,slit1_ch1,0.5)
    slit1_hfwhm,slit1_hcenter=exs.scanH(prefix,-slit1_start,-slit1_end,-slit1_step,slit1_ch0,slit1_ch1,0.5)

    # Log string
    print "Vertical = %8.1f Horizontal = %8.1f"%(slit1_vcenter,slit1_hcenter)
    logstr="Vertical = %8.1f Horizontal = %8.1f"%(slit1_vcenter,slit1_hcenter)
    logf.write("%s\n"%logstr)
    logf.flush()
    s.close()

    break
