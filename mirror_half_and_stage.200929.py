import sys, os, math
import socket
from Mirror import *
from MirrorTuneUnit import *
from Count import *
from MyException import *
from File import *
import Device_200929

# Make sure pin photodiode is swithced to No. 3 signal cable

if __name__ == "__main__":
    host = '172.24.242.41'
    dev = Device_200929.Device(host)
    dev.init()

    f = File("./")

    fname = "%03d_mirror_half.log" % f.getNewIdx3()
    ofile = open(fname, "w")

    # Skip flags
    #isSkipEvacStages = True
    isSkipEvacStages = False
    # Skip flags
    isSkipRecoverStages = False

    # Ensure
    # dummy_input = raw_input('Please ensure the PIN No.3 is connected to PicoAmp [ENTER]')

    # Preparation of mirror half
    if isSkipEvacStages:
        print "skipping stage movements"
    else:
        dev.prepMirrorHalf()

    # Ensure
    dummy_input = raw_input('Please Exit Exp2 and Open DSS [ENTER]')

    # D theta1 tune before mirror positional tuning
    dev.tuneDt1("./")

    # Slit1 open
    dev.slit1.openV()

    # Initial position
    init_y, init_z = dev.mirror.getYZ()
    print"Initial position (Y,Z)=(%7d,%7d)" % (init_y, init_z)

    ofile.write("Initial position (Y,Z)=(%7d,%7d)\n" % (init_y, init_z))

    # Mirror Evacuation (3 mm)
    dev.mirror.evacVFM_z()
    dev.mirror.evacHFM_y()

    # Current position
    curr_y, curr_z = dev.mirror.getYZ()
    print "Current position (Y,Z)=(%7d,%7d)\n" % (curr_y, curr_z)

    # Direct beam intensity
    dev.mtu.monDirPIN()
    # 2017/11/27 PIN photodiode for mirror unit
    i_dir, dummy = dev.countPin(pin_ch=1)
    ofile.write("Direct intensity:%5d\n" % i_dir)

    # VFM tune
    dev.mtu.monVFMPIN()
    dev.mirror.tuneVFM_z(init_z)
    i_vfm, dummy = dev.countPin(pin_ch=1)

    ofile.write("VMF intensity:%5d\n" % i_vfm)
    print "VFM scan finished"

    # HFM tune
    dev.mtu.monBothPIN()
    dev.mirror.tuneHFM_y(init_y)
    i_both, dummy = dev.countPin(pin_ch=1)
    ofile.write("Both intensity:%5d\n" % i_both)
    print "HFM scan finished"

    # Transmission calculation
    # Direct to vertical focusing
    trans_v = float(i_vfm) / float(i_dir)
    trans_h = float(i_both) / float(i_vfm)
    trans_both = float(i_both) / float(i_dir)
    ofile.write("Trans V: %8.5f H: %8.5f BOTH: %8.5f\n" % (trans_v, trans_h, trans_both))

    # Final position
    final_y, final_z = dev.mirror.getYZ()
    print"Final position (Y,Z)=(%7d,%7d)" % (final_y, final_z)
    ofile.write("Final position (Y,Z)=(%7d,%7d)\n" % (final_y, final_z))

    diff_y = final_y - init_y
    diff_z = final_z - init_z
    ofile.write("Diff (dy,dz)=(%7d,%7d)\n" % (diff_y, diff_z))

    # Translate both mirrors for matching relative configuration
    # VFM y should be moved by 'diff_y'
    curr_vfm_y = dev.mirror.getVFM_y()
    final_vfm_y = curr_vfm_y + diff_y
    dev.mirror.setVFM_y(final_vfm_y)

    curr_hfm_z = dev.mirror.getHFM_z()
    final_hfm_z = curr_hfm_z + diff_z
    dev.mirror.setHFM_z(final_hfm_z)
    print"Matching relative position of HFM and VFM"
    ofile.write("Moving VFM-Y from %7d to %7d\n" % (curr_vfm_y, final_vfm_y))
    ofile.write("Moving HFM-Z from %7d to %7d\n" % (curr_hfm_z, final_hfm_z))
    ofile.close()

    # Slit1 open
    dev.closeAllShutter()

    # Waiting for switching the PIN
    # dummy_input = raw_input('Please ensure the PIN No.6 is connected to PicoAmp[ENTER]')

    # Making log file for stage tuning
    fname = "%03d_stagetune.log" % f.getNewIdx3()
    ofile = open(fname, "w")

    if isSkipRecoverStages:
        print "skipping recover stages"
    else:
        # Move detectory-y and diffractometer stage to Original Y position
        dev.finishMirrorHalf()

    # Set Attenuator to 600um to scan diffractometer stage
    dev.setAttThick(600.0)

    # preparation of diffractometer scan
    dev.prepScanCoaxCam()

    # Get current YZ positions of diffractometer
    curr_sty = dev.stage.getYmm()
    curr_stz = dev.stage.getZmm()

    ofile.write("Sty=%12.5f Stz=%12.5f\n" % (curr_sty, curr_stz))

    # Scan
    fwhm_ymm, center_ymm = dev.stage.scanY("MOVE")
    fwhm_zmm, center_zmm = dev.stage.scanZ("MOVE")

    ofile.write("position Sty=%12.5f Stz=%12.5f\n" % (center_ymm, center_zmm))
    ofile.write("diameter Sty=%12.5f Stz=%12.5f\n" % (fwhm_ymm, fwhm_zmm))

    # Make sure
    ofile.close()
