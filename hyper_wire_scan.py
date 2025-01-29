#!/bin/env python import sys import socket
import time, os, math, sys
import math, numpy
import logging
import logging.config

sys.path.append("/isilon/BL32XU/BLsoft/PPPP")
import WireScan

if __name__ == "__main__":

    ws = WireScan.WireScan()
    ws.setDefaultPosition(-1.2329, -11.4233, -0.6979)

    ws.prepScan()

    # quick_option: exposure time for each point is set to 0.3 sec
    mean_y_size, mean_z_size, flux = ws.doSimpleScan(0.5, 0.040, n_times=1, quick_option=True)
    print(mean_y_size, mean_z_size, flux)
