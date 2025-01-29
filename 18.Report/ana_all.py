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
        self.isPrep = False
        self.required_files = ["CORRECT.LP", "XDS_ASCII.HKL"]
        
        self.isMTZ = False

    def addRequiredFile(self, filename):
        self.required_files.append(filename)

    def prep(self):
        adka = AnalyzeDirInKAMO.AnalyzeDirInKAMO(self.root_dir)

        # large wedge paths
        self.success_paths = adka.getGoodLargeWedgeDirs()
        
        # merge directories
        self.merge_dirs = adka.getMergeDirs()

        self.isPrep = True

    def makeReportLargeWedge(self, option = "None"):
        if self.isPrep == False:
            self.prep()
        arc_large = []

        if self.isMTZ == True:
            print self.isMTZ

        for ok in self.success_paths:
            for required_file in self.required_files:
                file_path = os.path.join(ok, required_file)
                if os.path.exists(file_path) == True:
                    rel_path = os.path.relpath(file_path, "./")
                    arc_large.append(rel_path)
                    if rel_path.rfind("XDS_ASCII.HKL")!=-1:
                        ana_dir = os.path.relpath(file_path)
                        print ana_dir
                        command = "cd %s\n xds2mtz.py\n cd %s \n " % (ana_dir, self.root_dir)
                        os.system(command)

        return arc_large

if __name__ == "__main__":
    option = sys.argv[1]

    tt = Toilet(".")
    print tt.makeReportLargeWedge()
