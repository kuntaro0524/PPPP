#!/bin/env python import sys import socket
import time, os, math, sys
import math, numpy
import logging
import logging.config

sys.path.append("/isilon/BL32XU/BLsoft/PPPP")
import File, Date
import AxesInfo
from pylab import *

# My library
import Device

class WireScan():
    def __init__(self, path="."):
        self.logpath = path
        self.dev = Device.Device("172.24.242.41")
        self.dev.init()
        # wire scan list
        self.tcs_list = [(0.026, 0.040), (0.05, 0.05), (0.1, 0.1), (0.2, 0.2), (0.3, 0.3), (0.5, 0.5)]
        self.enlist = [12.3984]

        #	Dtheta tune
        self.dthetaTuneFlag = True

        # Logging setting
        d = Date.Date()
        time_str = d.getNowMyFormat(option="date")
        logging.basicConfig(filename="wire_%s.log" % time_str, level=logging.DEBUG, format=FORMAT)

        logging.config.fileConfig('/isilon/BL32XU/BLsoft/PPPP/10.Zoo/Libs/logging.conf', defaults={'logfile_name': logname})
        self.logger = logging.getLogger('Tune')

        # Counter channel
        self.cnt_ch1 = 3
        self.cnt_ch2 = 0

        # File class
        self.f = File.File(self.logpath)

    def setDefaultPosition(self, sx, sy, sz):
        self.sx = sx
        self.sy = sy
        self.sz = sz

    def setTCSlist(self, tcs_list):
        self.tcs_list = tcs_list

    def setEnList(self, en_list):
        self.enlist = en_list

    ##	Usefull function
    def wire_rough_scan(self, sx, sy, sz):  # sx,sy,sz = wire default
        ## Wire rough scan
        ssz = sz + 0.1
        self.dev.gonio.moveXYZmm(sx, sy, ssz)
        xp, zp = self.dev.gonio.wireRoughZ(3)
        ssy = sy + 0.1
        self.dev.gonio.moveXYZmm(sx, ssy, sz)
        yp = self.dev.gonio.wireRoughY(3)

        # mm -> um
        xp = xp * 1000.0
        yp = yp * 1000.0
        zp = zp * 1000.0
        print "##### Wire Rough %8.5f %8.5f %8.5f\n" % (xp, yp, zp)

        return xp, yp, zp

    def setDefaultPosition(self, sx, sy, sz):
        self.sx = sx
        self.sy = sy
        self.sz = sz

    def goReady(self):
        ## 	Prep diffractometer for wire scan
        self.dev.slit1.closeV()
        self.dev.shutter.close()

    def prepScan(self, isColliOn=False):
        self.dev.prepScan(isColliOn)

    def expose(self):
        # Prep scan
        print "Ex1 slit moves to open position"
        self.dev.slit1.openV()
        print "Shutter open"
        self.dev.shutter.open()

    def scanColli(self):
        ## Collimator scan
        ## evacuation of a wire
        self.dev.gonio.moveXYZmm(sx, sy, sz)
        prefix = "%03d_colli" % (f.getNewIdx3())
        colli_y, colli_z = self.dev.colli.scan(prefix, 3)  # PIN after sample position
        cntstr_colli = self.dev.countPin(3)
        trans, pin = self.dev.colli.compareOnOff(3)
        return trans, pin

    def setCondition(self, tcsh, tcsv, yp, zp):
        # Check TCS aperture Horizontal
        if tcsh < 0.1:
            gstep_y = 0.1
            ssec_y = 2.0
            nstep_y = 100  #
        elif tcsh < 0.4:
            gstep_y = 0.5
            ssec_y = 2.0
            nstep_y = 30  #
        else:
            gstep_y = 1.0
            ssec_y = 2.0
            nstep_y = 20  #

        # Check TCS aperture Vertical
        if tcsv < 0.07:
            gstep_z = 0.1
            ssec_z = 2.0
            nstep_z = 100  #
        elif tcsv < 0.26:
            gstep_z = 0.2
            ssec_z = 2.0
            nstep_z = 50  #
        elif tcsv < 5.0:
            gstep_z = 0.5
            ssec_z = 2.0
            nstep_z = 50  #

        # Range parameters
        ystart = yp - float(nstep_y) * gstep_y
        yend = yp + float(nstep_y) * gstep_y
        zstart = zp - float(nstep_z) * gstep_z
        zend = zp + float(nstep_z) * gstep_z

        print "Scan Y range: %10.3f - %10.3f" % (ystart, yend)
        print "Scan Z range: %10.3f - %10.3f" % (zstart, zend)

        return gstep_y, gstep_z, ssec_y, ssec_z, nstep_y, nstep_z, ystart, yend, zstart, zend

    def tuneEnergy(self, energy):
        # Energy change
        self.dev.mono.changeE(energy)
        self.dev.id.moveE(energy)
        # Prefix of prefix
        prepre = "e%07.3f" % en

        if dthetaTuneFlag:
            prefix = "%03d_%s" % (f.getNewIdx3(), prepre)
            self.dev.mono.scanDt1PeakConfig(prefix, "DTSCAN_NORMAL", self.dev.tcs)

    def finishScan(self):
        self.dev.slit1.closeV()
        self.dev.id.moveE(12.3984)
        self.dev.mono.changeE(12.3984)

    def tuneGlancing(self, vfm_ty_center, scan_width=500, scan_step=50, ntimes=5):
        scan_wing = int(scan_width / 2.0)
        scan_start = vfm_ty_center - scan_wing
        scan_end = vfm_ty_center + scan_wing
        scan_range = numpy.arange(scan_start, scan_end, scan_step)

    def doScanAllSlitAperture(self, quick_option=False):


    def tuneHoriGlancing(self, center_hfm_tz_pls, scan_wing=1000, n_scan=5, quick_option=True):
        # scan range
        scan_start_pls = center_hfm_tz_pls - scan_wing
        scan_end_pls = center_hfm_tz_pls + scan_wing + 1.0
        step = (scan_wing * 2.0) / float(n_scan)

        # log file for horizontal glancing tune
        logfile = open("%03d_tune_HFMin.log" % self.f.getNewIdx3())

        for hfm_tz_pls in numpy.arange(scan_start_pls, scan_end_pls, step):
            self.dev.mirror.setHFMin(hfm_tz_pls)
            mean_y, mean_z, flux = self.doSimpleScan(0.026, 0.040, quick_option=quick_option)
            self.logger.info("HFM_TZ=%s\n" % hfm_tz_pls)
            self.logger.info("Y size=%s , Z size = %s\n" % (mean_y, mean_z))
            logfile.write("%5d,%10.6f,%10.6f, %10.6e\n" % (hfm_tz_pls, mean_y, mean_z, flux))
            self.logger.info("Next glancing angle...")

        logfile.close()

    def tuneHoriGlancing(self, center_hfm_tz_pls, scan_wing=1000, n_scan=5, quick_option=True):
        # scan range
        scan_start_pls = center_hfm_tz_pls - scan_wing
        scan_end_pls = center_hfm_tz_pls + scan_wing + 1.0
        step = (scan_wing * 2.0) / float(n_scan)

        # log file for horizontal glancing tune
        logfile = open("%03d_tune_HFMin.log" % self.f.getNewIdx3())

        for hfm_tz_pls in numpy.arange(scan_start_pls, scan_end_pls, step):
            self.logger.info("Next glancing angle.... HFM_tz=%8d" % hfm_tz_pls)
            self.dev.mirror.setVFMin(hfm_tz_pls)
            # All aperture of TCS
            for tcs_param in self.tcs_list:
                # Prep scan (All shutter is closed when the wire scan finished)
                # They should be opened here for loop experiments
                self.expose()

                # TCS aparture
                tcsv = float(tcs_param[0])
                tcsh = float(tcs_param[1])

                # TCS set aperture
                self.dev.tcs.setApert(tcsv, tcsh)

                # TCS str
                tcsstr = "%4.3fx%4.3f" % (tcsv, tcsh)

                # PREFIX
                prefix = "%03d_%s_%s" % (f.getNewIdx3(), "hfm_tz", tcsstr)
                mean_y, mean_z, flux = self.doSimpleScan(tcsv, tcsh, prefix, n_times=1,
                                                                   quick_option=quick_option)
                self.logger.info("hfm_tz=%s\n" % hfm_tz_pls)
                self.logger.info("TCS apert(V)=%10.6f (V)=%10.6f\n" % (tcsv, tcsh))
                self.logger.info("Mean beam size(Y)=%10.6f (Z)=%10.6f\n" % (mean_y, mean_z))
                logfile.write("%5d,%10.6f,%10.6f,%10.6f,%10.6f, %10.6e\n" % (hfm_tz_pls, tcsv, tcsh, mean_y, mean_z, flux))

    def tuneVertGlancing(self, center_vfm_ty_pls, scan_wing=1000, n_scan=5, quick_option=True):
        # scan range
        scan_start_pls = center_vfm_ty_pls - scan_wing
        scan_end_pls = center_vfm_ty_pls + scan_wing + 1.0
        step = (scan_wing * 2.0) / float(n_scan)

        # log file for horizontal glancing tune
        logfile = open("%03d_tune_VFMin.log" % self.f.getNewIdx3())

        for vfm_ty_pls in numpy.arange(scan_start_pls, scan_end_pls, step):
            self.logger.info("Next glancing angle.... VFM_ty=%8d" % vfm_ty_pls)
            self.dev.mirror.setVFMin(vfm_ty_pls)
            # All aperture of TCS
            for tcs_param in self.tcs_list:
                # Prep scan (All shutter is closed when the wire scan finished)
                # They should be opened here for loop experiments
                self.expose()

                # TCS aparture
                tcsv = float(tcs_param[0])
                tcsh = float(tcs_param[1])

                # TCS set aperture
                self.dev.tcs.setApert(tcsv, tcsh)

                # TCS str
                tcsstr = "%4.3fx%4.3f" % (tcsv, tcsh)

                # PREFIX
                prefix = "%03d_%s_%s" % (f.getNewIdx3(), "vfm_ty", tcsstr)
                mean_y, mean_z, flux = self.doSimpleScan(tcsv, tcsh, prefix, n_times=1,
                                                                   quick_option=quick_option)
                self.logger.info("VFM_TY=%s\n" % vfm_ty_pls)
                self.logger.info("TCS apert(V)=%10.6f (V)=%10.6f\n" % (tcsv, tcsh))
                self.logger.info("Beam size(Y)=%10.6f (Z)=%10.6f\n" % (mean_y, mean_z))
                logfile.write("%5d,%10.6f,%10.6f,%10.6f,%10.6f, %10.6e\n" % (vfm_ty_pls, tcsv, tcsh, mean_y, mean_z, flux))

    # Pulse base
    def doSimpleScan(self, tcsv, tcsh, prefix="scan", n_times=1, quick_option=False):

        # TCS set aperture
        self.logger.info("TCS aperture is set to %5.2f x %5.2f mm" % (tcsh, tcsv))
        self.dev.tcs.setApert(tcsv, tcsh)

        # Move wire to default position
        self.dev.gonio.moveXYZmm(self.sx, self.sy, self.sz)

        ysize_list = []
        zsize_list = []

        # Wire rough scan
        xp, yp, zp = self.wire_rough_scan(self.sx, self.sy, self.sz)  # sx,sy,sz = wire default
        self.logger.info("Wire rough position: %10.2f %10.2f %10.2f [um]" % (xp, yp, zp))

        for i in range(0, n_times):
            # Scan conditions
            gstep_y, gstep_z, ssec_y, ssec_z, nstep_y, nstep_z, ystart, yend, zstart, zend = self.setCondition(
                tcsh, tcsv, yp, zp)

            # quick scan for all conditions
            if quick_option:
                ssec_y = 0.2
                ssec_z = 0.2

            # set position
            tcsstr="%fx%f" % (tcsv, tcsh)
            prefix_y = "%03d_%s_gonioy_%s" % (self.f.getNewIdx3(), prefix, tcsstr)

            ywidth, ycenter = self.dev.gonio.scanYenc(prefix_y, ystart, yend, gstep_y, self.cnt_ch1, self.cnt_ch2, ssec_y)
            self.logger.info("Y width = %8.5f um (Y center=%10.5f )" % (ywidth, ycenter))
            ysize_list.append(ywidth)

            self.dev.gonio.moveXYZmm(self.sx, self.sy, self.sz)
            prefix_z = "%03d_%s_gonioz_%s" % (self.f.getNewIdx3(), prefix, tcsstr)
            zwidth, zcenter = self.dev.gonio.scanZenc(prefix_z, zstart, zend, gstep_z, self.cnt_ch1, self.cnt_ch2, ssec_z)
            self.logger.info("Z width = %8.5f um (Z center=%10.5f)" % (zwidth, zcenter))
            zsize_list.append(zwidth)

        # Mean beam size
        ya = numpy.array(ysize_list)
        za = numpy.array(zsize_list)
        mean_y_size = ya.mean()
        mean_z_size = za.mean()
        y_std = ya.std()
        z_std = za.std()

        self.logger.info("Mean Y size = %10.5f um (%8.5f)" % (mean_y_size, y_std))
        self.logger.info("Mean Z size = %10.5f um (%8.5f)" % (mean_z_size, z_std))

        flux = self.dev.measureFlux(finishScan=False)

        return mean_y_size, mean_z_size, flux

    def doMultiScan(self, direction="vertical", n_scan=5):
            logger = logging.logging()

            v_size_list = []
            h_size_list = []

            for glancing_v in glancing_v_list:
                self.setGlancing(glancing_v)
                mean_v_size = self.doVscan(n_scan)
                logger.info("mean V size = %8.5f at %s" % (mean_v_size, glancing_v))
                v_size_list.append(mean_v_size)

            for glancing_h in glancing_h_list:
                self.setGlancing(glancing_h)
                mean_h_size = self.doHscan(n_scan)
                logger.info("mean H size = %8.5f at %s" % (mean_h_size, glancing_h))
                h_size_list.append(mean_h_size)

    def doScan(self):
        # preparing the diffractometer
        self.goReady()

        ## 	Log file
        logname = "%03d_wire.log" % (f.getNewIdx3())
        logf = open(logname, "w")

        ## 	Wire scan
        for en in enlist:
            # Tune energy
            self.tuneEnergy()
            # Shutter open.
            self.expose()
            # Collimator scan
            trans, pin = self.scanColli()

            for tcs_param in self.tcs_list:
                # Prep scan (All shutter is closed when the wire scan finished)
                # They should be opened here for loop experiments
                self.expose()

                # TCS aparture
                tcsv = float(tcs_param[0])
                tcsh = float(tcs_param[1])

                # TCS set aperture
                self.dev.tcs.setApert(tcsv, tcsh)

                # TCS str
                tcsstr = "%4.3fx%4.3f" % (tcsv, tcsh)

                # PREFIX
                prefix = "%03d_%s_%s" % (f.getNewIdx3(), prepre, tcsstr)

                # Move wire to default position
                self.dev.gonio.moveXYZmm(self.sx, self.sy, self.sz)
                # Wire rough scan
                xp, yp, zp = self.wire_rough_scan(self.sx, self.sy, self.sz)  # sx,sy,sz = wire default
                print "Wire rough position: %10.2f %10.2f %10.2f [um]" % (xp, yp, zp)

                # Scan conditions
                gstep_y, gstep_z, ssec_y, ssec_z, nstep_y, nstep_z, ystart, yend, zstart, zend = self.setCondition(
                    tcsh, tcsv)

                # set position
                ywidth, ycenter = self.dev.gonio.scanYenc(prefix, ystart, yend, gstep_y, cnt_ch1, cnt_ch2, ssec_y)

                self.dev.gonio.moveXYZmm(sx, sy, sz)
                zwidth, zcenter = self.dev.gonio.scanZenc(prefix, zstart, zend, gstep_z, cnt_ch1, cnt_ch2, ssec_z)

                flux = self.measureFlux()

                logf.write(
                    "%8.4f %5.1f %5.1f %5.3f %5.3f %8.3f %8.3f %8.3f %8.3f %s ( Flux: %5.2e, Trans: %5.2f percent )\n" % (
                    en, colli_y, colli_z, tcsv, tcsh, zwidth, zcenter, ywidth, ycenter, cntstr, flux, trans))
                logf.flush()

                # Finishing scan before the next delta_theta1 tune
                print "Scan finished! Ex1 slit moves to close position"
                self.dev.slit1.closeV()
                print "Scan finished! Shutter moves to close position"
                self.dev.shutter.close()
            logf.close()

            break
        self.finishScan()

if __name__ == "__main__":
    # dev=Device("192.168.163.1")
    # dev = Device.Device("172.24.242.41")
    # dev.init()
    # dev.prepScan()
    # # dev.saveAxesInfo("axis.dat")
    ws = WireScan()
    ws.setDefaultPosition(-1.0172, -11.4120, -0.7420)
    tcs_list = [(0.1, 0.1)]
    ws.setTCSlist(tcs_list)

    ws.prepScan()
    mean_y_size, mean_z_size, flux = ws.doSimpleScan(0.1, 0.1, n_times=5)
    print(mean_y_size, mean_z_size, flux)