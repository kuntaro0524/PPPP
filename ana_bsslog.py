import sys, os, math, glob
import datetime, time
import DirectoryProc, AnaBSSlog

if __name__ == "__main__":
    anapath = "./"
    abl = AnaBSSlog.AnaBSSlog(anapath)
    
    loglist = glob.glob("%s/bss_*.log"%anapath)

    print loglist
    loglist.sort()

    for logfile in loglist:
        #print "Processing %s" % logfile
        abl.setLogFile(logfile)
        abl.readLogFile()
        collect_info, raster_info = abl.analyzeMeasurements()

        for colinfo in collect_info:
            print "DS:",colinfo
        for rasinfo in raster_info:
            print "RAS:",rasinfo
