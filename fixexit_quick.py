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
s.connect((host, port))

# Devices
id = ID(s)
mono = Mono(s)
tcs = TCS(s)
exs = ExSlit1(s)
axes = AxesInfo(s)
f = File("./")

curTy1=mono.getTy1()

# insert by YK at 140929 for restart script
# time.sleep(600)

while True:
    # St2Slit1 knife edge scan
    slit1_start = 18000
    slit1_end = 100
    slit1_step = -100
    slit1_ch0 = 3
    slit1_ch1 = 0

    # Detector number
    cnt_ch1 = 3
    cnt_ch2 = 0

    index = 0
    sizei = 0

    energy_list = [12.3984, 10.5, 18.0]
    #ty1_list = [2350, 2550]
    ty1_list = [2350, 2550, 2750]
    #ty1_list = [2570, 2770, 2970]

    ofile = open("fix_exit.log", "a")

    for energy in energy_list:
        # Starting time
        start_time = datetime.datetime.now()

        # Chenging energy
        mono.changeE(energy)
        id.moveE(energy)

        for ty1 in ty1_list:
            # Setting Ty1
            mono.moveTy1(ty1)

            # slit1 full open
            exs.fullOpen()

            ##  dtheta1 tune @ TCS 3.0mm x 3.0mm
            prefix = "%03d_%d_dtheta1" % (f.getNewIdx3(), ty1)
            dt1_fwhm, dt1_center = mono.scanDt1PeakConfig(prefix, "DTSCAN_FULLOPEN", tcs)

            exs.fullOpen()

            # Slit1 ty1 modification
            # rough & quick scan
            prefix = "%03d_rough" % f.getNewIdx3()
            slit1_final_step = slit1_step
            rough_step = slit1_final_step * 10
            rough_hfwhm, rough_hcenter = exs.scanH(prefix, -slit1_start, -slit1_end, -rough_step, slit1_ch0, slit1_ch1, 0.1)

            # Precise & narrow scan
            precise_start = rough_hcenter - slit1_step * 30
            precise_end = rough_hcenter + slit1_step * 30

            prefix = "%03d_precise" % f.getNewIdx3()

            #slit1_vfwhm, slit1_vcenter = exs.scanV(prefix, -slit1_start, -slit1_end, -slit1_step, slit1_ch0, slit1_ch1, 0.2)
            slit1_hfwhm, slit1_hcenter = exs.scanH(prefix, precise_start, precise_end, slit1_step, slit1_ch0, slit1_ch1, 0.1)

            end_time = datetime.datetime.now()

            d_time = end_time - start_time
            print d_time.seconds
            print "All time= %5.1f sec / Slit1 Hcenter %s " %(d_time.seconds, slit1_hcenter)

            logstr = "%20d[sec],%8.3f, %8d, %8d, %7.4f\n" %(d_time.seconds, energy, dt1_center, ty1, slit1_hcenter)
            ofile.write("%s" % logstr)
            ofile.flush()

    # Chenging energy back to 12.3984 keV #2021/04/05 added by mat
    mono.changeE(12.3984)
    id.moveE(12.3984)
    mono.moveTy1(curTy1)
    s.close()

    break
