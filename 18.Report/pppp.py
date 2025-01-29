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

class Toilet():

    def __init__(self, root_dir):
        self.root_dir = root_dir
        self.adka = AnalyzeDirInKAMO.AnalyzeDirInKAMO(root_dirroot_dir)

if __name__ == "__main__":
    #option = sys.argv[1]

    arc_files = []
    tl = Toilet(".")
    success_paths = tl.getGoodLargeWedgeDirs()
    required_files = ["CORRECT.LP", "XDS_ASCII.HKL"]
    for ok in success_paths:
        for required_file in required_files:
            file_path = os.path.join(ok, required_file)
            if os.path.exists(file_path) == True:
                rel_path = os.path.relpath(file_path, "./")
                arc_files.append(rel_path)

    # For merge directories
    merge_dirs = tl.getMergeDirs()
    for merge_dir in merge_dirs:
        print "MD=",merge_dir
