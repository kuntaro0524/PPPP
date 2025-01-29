import os,sys,math
sys.path.append("/isilon/BL32XU/BLsoft/PPPP/")

import Fitting
import AnaDSlog

if __name__ == "__main__":
    import sys

    ft=Fitting.Fitting()
    expected_half_ds=ft.fittingOnFile(sys.argv[1],1,2)

    an=AnaDSlog.AnaDSlog(sys.argv[2])
    phosec=float(sys.argv[3])
    print "Start estimation on AnaDSlog"
    logstr,limit_density=an.prep(phosec,expected_half_ds)
    print "End estimation on AnaDSlog"

    comment="Limit density = %5.1e photons/um^2"%limit_density
    ft.makePlotPNG("analyzed.png",comment=comment)

    print "%s %8.3e"%(sys.argv[1],limit_density)
