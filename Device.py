#!/bin/env python
import sys
import os
import socket
import time
import datetime

sys.path.append("/isilon/BL32XU/BLsoft/PPPP/")

from numpy import *

# My library
import Singleton
import File
import TCS
import BM
import Capture
import Count
import Mono
import ConfigFile
import Att
import BeamCenter
import Stage
import Zoom
import BS
import Shutter
import Cryo
import ID
import ExSlit1
import Light
import AnalyzePeak
import Gonio
import Colli
import Cover
import CCDlen
import CoaxPint
import MBS
import DSS
import BeamsizeConfig
import Flux
import Mirror
import MirrorTuneUnit
import MyException
import DetectorStage
import Motor
import logging
import logging.config

class Device(Singleton.Singleton):
    def __init__(self, server_address):
        self.isInit = False
        host = server_address
        port = 10101
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((host, port))
        # logging.config.fileConfig('/isilon/BL32XU/BLsoft/PPPP/10.Zoo/Libs/logging.conf', defaults={'logfile_name': logname})
        self.logger = logging.getLogger('Tune').getChild("Device")

    def readConfig(self):
        conf = ConfigFile.ConfigFile()
        # Reading config file
        try:
            ## Dtheta 1
            self.scan_dt1_ch1 = int(conf.getCondition2("DTSCAN", "ch1"))
            self.scan_dt1_ch2 = int(conf.getCondition2("DTSCAN", "ch2"))
            self.scan_dt1_start = int(conf.getCondition2("DTSCAN", "start"))
            self.scan_dt1_end = int(conf.getCondition2("DTSCAN", "end"))
            self.scan_dt1_step = int(conf.getCondition2("DTSCAN", "step"))
            self.scan_dt1_time = conf.getCondition2("DTSCAN", "time")

            ## Fixed point parameters
            self.fixed_ch1 = int(conf.getCondition2("FIXED_POINT", "ch1"))
            self.fixed_ch2 = int(conf.getCondition2("FIXED_POINT", "ch2"))
            self.block_time = conf.getCondition2("FIXED_POINT", "block_time")
            self.total_num = conf.getCondition2("FIXED_POINT", "total_num")
            self.count_time = conf.getCondition2("FIXED_POINT", "time")

        except MyException, ttt:
            print ttt.args[0]
            print "Check your config file carefully.\n"
            sys.exit(1)

    def init(self):
        # settings
        self.mono = Mono.Mono(self.s)
        self.tcs = TCS.TCS(self.s)
        self.bm = BM.BM(self.s)
        self.f = File.File("./")
        self.capture = Capture.Capture()
        self.slit1 = ExSlit1.ExSlit1(self.s)
        self.att = Att.Att(self.s)
        self.stage = Stage.Stage(self.s)
        self.zoom = Zoom.Zoom(self.s)
        self.bs = BS.BS(self.s)
        self.cryo = Cryo.Cryo(self.s)
        self.id = ID.ID(self.s)
        self.light = Light.Light(self.s)
        self.gonio = Gonio.Gonio(self.s)
        self.colli = Colli.Colli(self.s)
        self.coax_pint = CoaxPint.CoaxPint(self.s)
        self.clen = CCDlen.CCDlen(self.s)
        self.covz = Cover.Cover(self.s)
        self.shutter = Shutter.Shutter(self.s)
        self.mirror = Mirror.Mirror(self.s)
        self.mtu = MirrorTuneUnit.MirrorTuneUnit(self.s)
        self.det_y = DetectorStage.DetectorStage(self.s)

        # self.readConfig()
        # Optics
        self.mbs = MBS.MBS(self.s)
        self.dss = DSS.DSS(self.s)

        print "Device. initialization finished"
        self.isInit = True

    # comment out by YK 161031
    #	def waitAndOpenOptShutters(self):

    def getServer(self):
        return self.s

    def calcFlux(self, en, pin_uA):
        fluxer = Flux.Flux(en)
        flux = fluxer.calcFluxFromPIN(pin_uA)
        return flux

    def tuneDt1(self, logpath):
        if os.path.exists(logpath) == False:
            os.makedirs(logpath)
        self.f = File.File(logpath)
        prefix = "%s/%03d" % (logpath, self.f.getNewIdx3())
        self.mono.scanDt1PeakConfig(prefix, "DTSCAN_NORMAL", self.tcs)
        dtheta1 = int(self.mono.getDt1())
        print "Final dtheta1 = %d pls" % dtheta1

    def changeEnergy(self, en, isTune=True, logpath="/isilon/BL32XU/BLsoft/Logs/Zoo/"):
        # Energy change
        self.mono.changeE(en)
        # Gap
        self.id.moveE(en)
        if isTune == True:
            self.tuneDt1(logpath)

    def measureFlux(self, finishScan=True):
        en = self.mono.getE()
        # collimator on
        self.colli.on()
        # Prep scan
        self.prepScan()
        # Measurement
        ipin, iic = self.countPin(pin_ch=3)
        pin_uA = ipin / 100.0
        iic_nA = iic / 100.0
        # Photon flux estimation
        ff = Flux.Flux(en)
        phosec = ff.calcFluxFromPIN(pin_uA)
        if finishScan:
            self.finishScan(cover_off=True)
        else:
            pass

        return phosec

    def getBeamsize(self, config_dir="/isilon/blconfig/bl32xu/"):
        tcs_vmm, tcs_hmm = self.tcs.getApert()
        bsf = BeamsizeConfig.BeamsizeConfig(config_dir)
        hbeam, vbeam = bsf.getBeamsizeAtTCS_HV(tcs_hmm, tcs_vmm)
        return hbeam, vbeam

    def bsOff(self):
        if self.isInit == False:
            self.init()
        self.bs.off()

    def prepScan(self, isColliOn=False):
        # Prep scan
        self.clen.evac()
        ## Cover on
        try:
            self.covz.on()
        except MyException, ttt:
            # raise MyException("CCD camera cover cannot be inserted.")
            self.logger.info("inPrepScan CCD camera cover error.")
            sys.exit(1)

        time.sleep(2.0)
        ## Cover check
        self.covz.isCover()
        self.light.off()
        self.shutter.open()
        self.slit1.openV()
        ## Attenuator
        self.att.setAttThick(0)
        ## BS off
        self.bs.off()
        if isColliOn == False:
            self.colli.off()
        else:
            ## Collimator in
            self.colli.on()

    def prepScanCoaxCam(self):
        # Prep scan
        self.clen.evac()
        ## Cover on
        self.covz.on()
        time.sleep(2.0)
        ## Cover check
        self.covz.isCover()
        self.light.off()
        self.slit1.openV()
        ## BS off
        self.bs.off()
        self.colli.off()
        self.shutter.open()

    def finishScan(self, cover_off=True):
        self.shutter.close()
        self.slit1.closeV()
        self.colli.off()
        if cover_off == True:
            ## Cover off
            self.covz.off()

    def closeAllShutter(self):
        self.shutter.close()
        self.slit1.closeV()

    def countPin(self, pin_ch=3):
        counter = Count.Count(self.s, pin_ch, 0)
        i_pin, i_ion = counter.getCount(1.0)
        return i_pin, i_ion

    def countOneSec(self, ch=0):
        counter = Count.Count(self.s, ch, 1)
        t_value, dummy = counter.getCount(1.0)
        return t_value

    def setAttThick(self, thick):
        if self.isInit == False:
            self.init()
        self.att.setAttThick(thick)

    def calcAttFac(self, wl, thickness):
        self.att.calcAttFac(wl, thickness)

    def closeShutters(self):
        self.slit1.closeV()
        self.shutter.close()

    def openShutters(self):
        self.slit1.openV()
        self.shutter.open()

    def prepView(self):
        if self.isInit == False:
            self.init()
        self.closeShutters()
        self.light.on()

    def moveGonioXYZ(self, x, y, z):
        self.gonio.moveXYZmm(x, y, z)

    def prepCentering(self):
        self.bs.off()
        self.colli.off()
        self.light.on()

    def prepBM(self):
        if self.isInit == False:
            self.init()
        self.covz.on()
        self.colli.goOff()
        self.bs.goOn()
        ## Zoom in
        self.zoom.go(0)
        ## BM on
        self.bm.onPika()
        ## Shutter open
        self.openShutters()

    def finishBM(self):
        if self.isInit == False:
            self.init()
        self.closeAllShutter()
        self.bm.offXYZ()
        self.covz.off()

    ################################
    # Last modified 120607
    # for XYZ stage implemtented to the monitor
    ################################
    def prepCapture(self):
        if self.isInit == False:
            self.init()
        ## Zoom in
        self.zoom.go(0)

        ## Cryo go up
        self.cryo.off()

        ## BM on
        self.bm.onPika()

        ## BS on
        self.bs.on()

    ###########################
    # Last modified 120607
    # for XYZ stage implemtented to the monitor
    ###########################
    def finishCapture(self):
        if self.isInit == False:
            self.init()
        ## BM off
        self.bm.offXYZ()
        ## BS off
        self.bs.off()

    def captureBM(self, prefix, isTune=True):
        if self.isInit == False:
            self.init()

        # Attenuator setting
        if isTune == True:
            # Tune gain
            gain = self.cap.tuneGain()

        print "##### GAIN %5d\n" % gain

        ### averaging center x,y
        path = os.path.abspath("./")
        prefix = "%s/%s" % (path, prefix)
        x, y = self.cap.aveCenter(prefix, 5)

        return x, y

    def prepMirrorHalf(self):
        self.det_y.evacuate()
        self.stage.stageEvac()

    def finishMirrorHalf(self):
        curr_ymm = self.stage.getYmm()
        target_ymm = curr_ymm - 200.0
        self.stage.setYmm(target_ymm)
        self.det_y.moveToOrigin()

    def setHyperFocus(self, output_path, d_mv_ty_pls=2500, d_mh_tz_pls=400):
        self.f = File.File(output_path)
        prefix = "%s/%03d" % (output_path, self.f.getNewIdx3())
        logf = open("%s_hyper_focus.log"%prefix, "w")
        # Saving current positions
        # stagey, stagez, mh_tz, mv_ty
        curr_sty = self.stage.getYmm()
        curr_stz = self.stage.getZmm()
        curr_mv_ty = self.mirror.getVFMin()
        curr_mh_tz = self.mirror.getHFMin()
        # logfile
        logf.write("Date Time %s\n" % datetime.datetime.now())
        logf.write("stage Y = %9.5f mm\n" % curr_sty)
        logf.write("stage Z = %9.5f mm\n" % curr_stz)
        logf.write("Mirror glancing (Mv theta-y) = %9d pls\n" % curr_mv_ty)
        logf.write("Mirror glancing (Mh theta-z) = %9d pls\n" % curr_mh_tz)

        #d_mv_ty_pls = +2500 # pls
        #d_mh_tz_pls = +400 # pls

        # Back lash

        # For hyper focusing given by arguments
        # Aimed position of mv_ty, mh_tz
        target_mv_ty = curr_mv_ty + d_mv_ty_pls
        target_mh_tz = curr_mh_tz + d_mh_tz_pls

        # Aimed position of stage Y/Z
        d_sty = -0.0174 # mm
        d_stz = +0.239 # mm
        rough_sty = curr_sty + d_sty
        rough_stz = curr_stz + d_stz

        print target_mv_ty, target_mh_tz, rough_sty, rough_stz

        # Shutter close
        self.closeAllShutter()

        # Moving glancing angle
        # back lash
        self.mirror.setHFMin(target_mh_tz-500)
        self.mirror.setVFMin(target_mv_ty-500)
        # set
        self.mirror.setHFMin(target_mh_tz)
        self.mirror.setVFMin(target_mv_ty)
        self.stage.setYmm(rough_sty)
        self.stage.setZmm(rough_stz)

        logf.write("### After relative movements based on the previous information ###\n")
        logf.write("stage Y = %9.5f mm\n" % rough_sty)
        logf.write("stage Z = %9.5f mm\n" % rough_stz)
        logf.write("Mirror glancing (Mv theta-y) = %9d pls\n" % target_mv_ty)
        logf.write("Mirror glancing (Mh theta-z) = %9d pls\n" % target_mh_tz)

    def evacuate(self):
        self.moveY(self.evacuate_position)

    def moveToOrigin(self):
        self.moveY(self.in_position)

    # usage: after shutter
    def simpleCountBack(self, ch1, ch2, inttime, ndata):
        if self.isInit == False:
            self.init()
        # shutter close
        print "Shutter close: estimation of background"
        self.closeShutters()
        # average back ground
        ave1, ave2 = self.simpleCount(ch1, ch2, inttime, ndata)

        # shutter open
        self.openShutters()
        print "Shutter open: estimation of actual count"
        ave3, ave4 = self.simpleCount(ch1, ch2, inttime, ndata, ave1, ave2)

        print "Average ch1: %8d ch2: %8d\n" % (ave3, ave4)
        return ave3, ave4

    def simpleCount(self, ch1, ch2, inttime, ndata, back1=0, back2=0):
        if self.isInit == False:
            self.init()
        counter = Count.Count(self.s, ch1, ch2)
        f = File.File("./")

        prefix = "%03d" % f.getNewIdx3()
        ofilename = "%s_count.scn" % prefix
        of = open(ofilename, "w")

        # initialization
        starttime = time.time()
        strtime = datetime.datetime.now()
        of.write("#### %s\n" % starttime)
        of.write("#### %s\n" % strtime)
        ttime = 0
        for i in arange(0, ndata, 1):
            currtime = time.time()
            ttime = currtime - starttime
            ch1, ch2 = counter.getCount(inttime)
            ch1 = ch1 - back1
            ch2 = ch2 - back2
            of.write("12345 %8.4f %12d %12d\n" % (ttime, ch1, ch2))
        of.close()

        # file open
        ana = AnalyzePeak.AnalyzePeak(ofilename)
        x, y1, y2 = ana.prepData3(1, 2, 3)

        py1 = ana.getPylabArray(y1)
        py2 = ana.getPylabArray(y2)

        mean1 = py1.mean()
        mean2 = py2.mean()
        std1 = py1.std()
        std2 = py2.std()

        of = open(ofilename, "a")

        of.write("COUNTER1:%5d Average: %12.5f Std.:%12.5f (%8.3f perc.)\n" % (
        ch1, py1.mean(), py1.std(), py1.std() / py1.mean() * 100.0))
        of.write("COUNTER2:%5d Average: %12.5f Std.:%12.5f (%8.3f perc.)\n" % (
        ch2, py2.mean(), py2.std(), py2.std() / py2.mean() * 100.0))

        of.close()
        return mean1, mean2

    def saveAxesInfo(self, ofname):
        d = datetime.datetime.today()

        ofile = open(ofname, "w")
        ofile.write("### %s ####\n" % d)
        ofile.write("##### ID #####\n")
        ofile.write("ID gap\t:%12s%7s\n" % Motor.Motor(self.s, "bl_32in_id_gap", "mm").getPosition())
        ofile.write("##### Front End ####\n")
        ofile.write("vert\t:%12s%7s\n" % Motor.Motor(self.s, "bl_32in_fe_slit_1_vertical", "mm").getPosition())
        ofile.write("hori\t:%12s%7s\n" % Motor.Motor(self.s, "bl_32in_fe_slit_1_horizontal", "mm").getPosition())
        ofile.write("height\t:%12s%7s\n" % Motor.Motor(self.s, "bl_32in_fe_slit_1_height", "mm").getApert())
        ofile.write("width\t:%12s%7s\n" % Motor.Motor(self.s, "bl_32in_fe_slit_1_width", "mm").getApert())
        ofile.write("##### Monochromator ####\n")
        ofile.write("Energy\t:%12s%7s\n" % Motor.Motor(self.s, "bl_32in_tc1_stmono_1", "pulse").getEnergy())
        ofile.write("Angle\t:%12s%7s\n" % Motor.Motor(self.s, "bl_32in_tc1_stmono_1", "pulse").getAngle())
        ofile.write("Wavelength\t:%12s%7s\n" % Motor.Motor(self.s, "bl_32in_tc1_stmono_1", "pulse").getRamda())
        ofile.write("Theta\t:%12s%7s\n" % Motor.Motor(self.s, "bl_32in_tc1_stmono_1_theta", "pulse").getPosition())
        ofile.write("Y1\t:%12s%7s\n" % Motor.Motor(self.s, "bl_32in_tc1_stmono_1_y1", "pulse").getPosition())
        ofile.write("Z1\t:%12s%7s\n" % Motor.Motor(self.s, "bl_32in_tc1_stmono_1_z1", "pulse").getPosition())
        ofile.write("Dth1\t:%12s%7s\n" % Motor.Motor(self.s, "bl_32in_tc1_stmono_1_dtheta1", "pulse").getPosition())
        ofile.write("Ty1\t:%12s%7s\n" % Motor.Motor(self.s, "bl_32in_tc1_stmono_1_thetay1", "pulse").getPosition())
        ofile.write("Z2\t:%12s%7s\n" % Motor.Motor(self.s, "bl_32in_tc1_stmono_1_z2", "pulse").getPosition())
        ofile.write("Tx2\t:%12s%7s\n" % Motor.Motor(self.s, "bl_32in_tc1_stmono_1_thetax2", "pulse").getPosition())
        ofile.write("Ty2\t:%12s%7s\n" % Motor.Motor(self.s, "bl_32in_tc1_stmono_1_thetay2", "pulse").getPosition())
        ofile.write("Xt\t:%12s%7s\n" % Motor.Motor(self.s, "bl_32in_tc1_stmono_1_xt", "pulse").getPosition())
        ofile.write("Zt\t:%12s%7s\n" % Motor.Motor(self.s, "bl_32in_tc1_stmono_1_zt", "pulse").getPosition())
        ofile.write("##### TC slit ####\n")
        ofile.write("height\t:%12s%7s\n" % Motor.Motor(self.s, "bl_32in_tc1_slit_1_height", "mm").getApert())
        ofile.write("width\t:%12s%7s\n" % Motor.Motor(self.s, "bl_32in_tc1_slit_1_width", "mm").getApert())
        ofile.write("vert\t:%12s%7s\n" % Motor.Motor(self.s, "bl_32in_tc1_slit_1_vertical", "mm").getPosition())
        ofile.write("hori\t:%12s%7s\n" % Motor.Motor(self.s, "bl_32in_tc1_slit_1_horizontal", "mm").getPosition())
        ofile.write("##### Mirror ####\n")
        ofile.write("VFM-y\t:%12s%7s\n" % Motor.Motor(self.s, "bl_32in_st2_mv_1_y", "pulse").getPosition())
        ofile.write("VFM-z\t:%12s%7s\n" % Motor.Motor(self.s, "bl_32in_st2_mv_1_z", "pulse").getPosition())
        ofile.write("VFM-tx\t:%12s%7s\n" % Motor.Motor(self.s, "bl_32in_st2_mv_1_tx", "pulse").getPosition())
        ofile.write("VFM-ty\t:%12s%7s\n" % Motor.Motor(self.s, "bl_32in_st2_mv_1_ty", "pulse").getPosition())
        ofile.write("HFM-y\t:%12s%7s\n" % Motor.Motor(self.s, "bl_32in_st2_mh_1_y", "pulse").getPosition())
        ofile.write("HFM-z\t:%12s%7s\n" % Motor.Motor(self.s, "bl_32in_st2_mh_1_z", "pulse").getPosition())
        ofile.write("HFM-tz\t:%12s%7s\n" % Motor.Motor(self.s, "bl_32in_st2_mh_1_tz", "pulse").getPosition())
        ofile.write("##### Stage ####\n")
        ofile.write("Stage-y\t:%12s%7s\n" % Motor.Motor(self.s, "bl_32in_st2_stage_1_y", "pulse").getPosition())
        ofile.write("Stage-z\t:%12s%7s\n" % Motor.Motor(self.s, "bl_32in_st2_stage_1_z", "pulse").getPosition())
        ofile.write("Coax-x\t:%12s%7s\n" % Motor.Motor(self.s, "bl_32in_st2_coax_1_x", "pulse").getPosition())
        ofile.write("Coax-y\t:%12s%7s\n" % Motor.Motor(self.s, "bl_32in_st2_slit_2_ring", "pulse").getPosition())
        ofile.write("Coax-z\t:%12s%7s\n" % Motor.Motor(self.s, "bl_32in_st2_slit_2_hall", "pulse").getPosition())
        ofile.write("Gonio phi\t:%12s%7s\n" % Motor.Motor(self.s, "bl_32in_st2_gonio_1_phi", "pulse").getPosition())
        ofile.write("Gonio x\t:%12s%7s\n" % Motor.Motor(self.s, "bl_32in_st2_gonio_1_x", "pulse").getPosition())
        ofile.write("Gonio y\t:%12s%7s\n" % Motor.Motor(self.s, "bl_32in_st2_gonio_1_y", "pulse").getPosition())
        ofile.write("Gonio z\t:%12s%7s\n" % Motor.Motor(self.s, "bl_32in_st2_gonio_1_z", "pulse").getPosition())
        ofile.write("Gonio zz\t:%12s%7s\n" % Motor.Motor(self.s, "bl_32in_st2_gonio_1_zz", "pulse").getPosition())

        ofile.close()

        return True

if __name__ == "__main__":
    # dev=Device("192.168.163.1")
    dev = Device("172.24.242.41")
    dev.init()

    # logpath="/isilon/users/target/target/Staff/2016B/161003/03.Test/"

    count_time = 1.0
    dev.simpleCountBack(3, 0, count_time, 1)

    """
        if os.path.exists(logpath)==False:
                os.makedirs(logpath)
    print "%e"%dev.measureFlux(logpath,tune=False,config_dir="/isilon/blconfig/bl32xu/bss/")
    """
    # dev.tcs.setApert(0.1,0.1)
    # phosec=dev.measureFlux()

    # dev.prepCapture()
    # dev.finishCapture()

    # print "%e"%phosec
    # hbeam,vbeam=dev.getCurrentBeamsize(config_dir="/isilon/blconfig/bl32xu/")
    # print phosec,hbeam,vbeam

    dev.closeAllShutter()

# print proc.gonio.getXYZmm()
# dev.finishMirrorHalf()
# dev.finishMirrorHalf()
# proc.bsOff()
# print proc.captureBM("TEST")
# en_list=arange(19.5,8.0,-0.5)
# print en_list,len(en_list)

# en_list=[19.5,15.5,12.5,11.5,11.0,10.5,10.4,10.3,10.2,10.1,10.0,9.9,9.8,9.7,9.6,9.5,8.5]
# en_list=[19.5,15.5,12.3984,11.5,10.5,9.5,8.5]
# en_list=[8.5,9.5,10.5,11.5,12.3984,15.5,19.5]
# en_list=arange(8.5,11.0,0.1)
# print en_list
# print len(en_list)

# while(1):
# for en in en_list:
# proc.makeTable(en)

# Analyze knife
# print proc.analyzeKnife("049_stagey.scn")

# Energy table check
# proc.moveEtable(8.5)
