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

    # TCS size list for tuning glancing angle.
    tcs_list = [(0.026, 0.040), (0.5, 0.5)]
    ws.setTCSlist(tcs_list)

    # Scan preparation
    ws.prepScan(isColliOn=False)

    # Tuning horizontal tz parameter
    center_hfm_tz_pls = 165791
    ws.tuneHoriGlancing(center_hfm_tz_pls, scan_wing=500, n_scan=3, quick_option=True)
    center_vfm_ty_pls = 288700
    ws.tuneVertGlancing(center_vfm_ty_pls, scan_wing=500, n_scan=5, quick_option=True)