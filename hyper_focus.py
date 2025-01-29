#!/bin/env python
import sys
import os
import socket
import time
import datetime

sys.path.append("/isilon/BL32XU/BLsoft/PPPP/")

from numpy import *

# My library
import Device

if __name__ == "__main__":
    dev = Device.Device("172.24.242.41")
    dev.init()

    # directory for log files
    logpath="./"
    dev.saveAxesInfo("axesinfo_before.dat")
    dev.setHyperFocus(logpath, d_mv_ty_pls=2500, d_mh_tz_pls=0)
    dev.saveAxesInfo("axesinfo_after.dat")
