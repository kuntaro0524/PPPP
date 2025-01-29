import sys,os
sys.path.append("/isilon/BL32XU/BLsoft/PPPP/")
sys.path.append("/isilon/BL32XU/BLsoft/PPPP/11.ClusterAnalysis/")
sys.path.append("/isilon/BL32XU/BLsoft/PPPP/18.Report/")

import glob,numpy
import DirectoryProc
import MyDate
import time
import XSCALEReporter

# DEBUG flag
isDebug = False
isIncludeMTZ = False

class AnalyzeDirInKAMO():
    def __init__(self, root_dir):
        self.root_dir = root_dir
        self.isPrep = False

    def evaluate_largewedge(self, dires):
        print "HHHHHHHHHHHHHHHHHHHHHHHHH"
        ok_paths = []
        bad_paths = []
        n_all = len(dires)
        for d in dires:
            check_file = "%s/CORRECT.LP" % d
            if os.path.exists(check_file) == True:
                ok_paths.append(d)
            else:
                bad_paths.append(d)
    
        return ok_paths, bad_paths
    
    def prep(self):
        # store all of directories here
        dp = DirectoryProc.DirectoryProc(".")
        dirs = dp.findDirs()

        self.merge_dirs = []
        # Merge-related directoryies
        for d in dirs:
            if d.startswith("merge") == True:
                self.merge_dirs.append(d)

        # Finding data processing directory
        self.found_procd = []

        # For large wedge data 
        for heredir in dirs:
            pp = DirectoryProc.DirectoryProc(heredir)
            # Directory search in the directory here
            qq = pp.findDirs()
            # Check root_dir/path1/path2/:(path2 = q)
            for q in qq:
                max_index = -9999
                # Data directory exists
                if q.rfind("data") != -1:
                    cols = q.split('/')
                    index_str = cols[-1].replace("data","")
                    #print int(index_str)
                    max_index = int(index_str)
                    #print max_index
                    #print mpath
                if max_index != -9999:
                    ddir_abs = os.path.abspath(heredir)
                    #print ddir_abs
                    found_d = "%s/%s/" % (ddir_abs, q)
                    #print "EEEEE",found_d
                    self.found_procd.append(found_d)
                else:
                    print "No data processed: %s" % q

        self.isPrep = True
        return self.found_procd

    def getMergeDirs(self):
        if self.isPrep == False:
            self.prep()
        return self.merge_dirs

    def getGoodLargeWedgeDirs(self):
        if self.isPrep == False:
            self.prep()
        # For multiple small wedge datasets
        self.multi_dirs = []
        self.largewedge_dirs = []
        for procd_abs in self.found_procd:
            ddd = DirectoryProc.DirectoryProc(procd_abs)
            procd_dirs = ddd.findDirs()
            
            for procd in procd_dirs:
                if procd.rfind("multi") != -1:
                    final_path = os.path.join(procd_abs, procd)
                    self.multi_dirs.append(final_path)
                else:
                    final_path = os.path.join(procd_abs, procd)
                    self.largewedge_dirs.append(final_path)
        
        print "MULTI NDS = ", len(self.multi_dirs)
        print "LARGE NDS = ", len(self.largewedge_dirs)
        #print "MERGE DIR = ", len(self.merge_dirs)

        # CORRECT.LP existing data processing paths.
        success_paths, bad_paths = self.evaluate_largewedge(self.largewedge_dirs)

        return success_paths

if __name__ == "__main__":
    arc_files = []
    jw = AnalyzeDirInKAMO("./")
    success_paths = jw.getGoodLargeWedgeDirs()
    required_files = ["CORRECT.LP", "XDS_ASCII.HKL"]
    arc_command = "tar cvfz ttttt.tgz "
    for ok in success_paths:
        for required_file in required_files:
            file_path = os.path.join(ok, required_file)
            if os.path.exists(file_path) == True:
                rel_path = os.path.relpath(file_path, "./")
                #print "RRRRR=",rel_path
                arc_files.append(rel_path)
                arc_command += "%s " % rel_path
    
    print arc_command
    #os.system(arc_command)
