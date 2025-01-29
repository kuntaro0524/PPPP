import socket
import time
import datetime

# My library
import Morning


def time_now():
    strtime = datetime.datetime.now().strftime("%H:%M:%S")
    return strtime


def date_now():
    strtime = datetime.datetime.now().strftime("%Y%m%d-%H%M")
    return strtime


if __name__ == "__main__":
    mng = Morning.Morning("./")

    # Beam position log
    bplogname = "/isilon/BL32XU/BLsoft/Logs/beam.log"
    bplog = open(bplogname, "aw")

    # Morning log file
    tstr = datetime.datetime.now().strftime("%Y-%m-%d-%H%M")
    fname = "MT_%s.dat" % tstr
    logf = open(fname, "w")

    # Scintillator set position
    mng.prepBC()

    # Open shutter
    print "PREP"
    mng.prepScan()

    # ST-Y tune
    print "STY tune started"
    sty_curr, sty_tuned = mng.stageYtuneCapture()
    d_sty = (sty_tuned - sty_curr) * 1000.0  # [um]
    logf.write("%10s %10s PREV=%9.4f CURR=%9.4f Diff=%10.4f[um]\n" % (time_now(), "St-y", sty_curr, sty_tuned, d_sty))
    logf.flush()

    # def doCapAna(self,prefix,avetime=10,nrepeat=1,thicktune=True):
    picy, picz = mng.doCapAna("morning", 10, 1, False)

    mng.saveBP(picy, picz)
    logf.write("%10s %10s code (Y,Z) = (%5d,%5d)\n" % (time_now(), "BeamCen", picy, picz))
    logf.flush()

    # Finish (remove beam monitor)
    mng.finishBC()
    mng.finishExposure()

    mng.allFin()
    logf.close()

# Evacuate all for manual unmount
