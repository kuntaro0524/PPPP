import sys,os
sys.path.append("/isilon/BL32XU/BLsoft/PPPP/")
sys.path.append("/isilon/BL32XU/BLsoft/PPPP/11.ClusterAnalysis/")
sys.path.append("/isilon/BL32XU/BLsoft/PPPP/18.Report/")

import glob,numpy
import DirectoryProc
import MyDate
import time
import XSCALEReporter
import AnalyzeDirInKAMO

# DEBUG flag
isDebug = False
isIncludeMTZ = False

if __name__ == "__main__":
    # Making archive commend
    da = MyDate.MyDate()
    dstr = da.getNowMyFormat(option="other")
    prefix = sys.argv[1]
    tgz_file = "%s_%s.tgz " % (dstr, prefix)

    arc_files = []
    jw = AnalyzeDirInKAMO.AnalyzeDirInKAMO("./")
    success_paths = jw.getMultiDirs()
    required_files = ["CORRECT.LP", "XDS_ASCII.HKL"]

    arc_command = "tar cvfz %s " % tgz_file
    for ok in success_paths:
        for required_file in required_files:
            file_path = os.path.join(ok, required_file)
            if os.path.exists(file_path) == True:
                rel_path = os.path.relpath(file_path, "./")
                arc_files.append(rel_path)
                arc_command += "%s " % rel_path

    os.system(arc_command)

