import sys,os
sys.path.append("/isilon/BL32XU/BLsoft/PPPP/Libs/")
sys.path.append("/isilon/BL32XU/BLsoft/PPPP/")
sys.path.append("/isilon/BL32XU/BLsoft/PPPP/11.ClusterAnalysis/")
sys.path.append("/isilon/BL32XU/BLsoft/PPPP/18.Report/")

import MyException
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
        self.isDebug = True
        # Dictionary for directories (type and directory name)
        self.dir_dict = {}

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
        # store all of directories in the designated path.
        dp = DirectoryProc.DirectoryProc(self.root_dir)
        dirs = dp.findDirs()

        if self.isDebug: print "Directory list in root_dir=", dirs, "in %s" % self.root_dir

        self.merge_dirs = []
        # Merge-related directoryies
        for d in dirs:
            if d.startswith("merge") == True:
                abs_path_merge = os.path.abspath(d)
                self.merge_dirs.append(abs_path_merge)

        self.dir_dict["merge"] = self.merge_dirs

        # Finding data processing directory
        self.found_procd = []

        # For large wedge data 
        # _kamoproc/CPS1416-01/ : pin_dir = "CPS1416-01"
        print ("Large wedge directory analysis")
        for pin_dir in dirs:
            abs_pin_dir = os.path.join(self.root_dir, pin_dir)
            pp = DirectoryProc.DirectoryProc(abs_pin_dir)
            # Directory search in the directory here
            qq = pp.findDirs()
            # Check root_dir/path1/path2/:(path2 = q)
            # /isilon/users/target/target/AutoUsers/200218/ariyoshi/_kamoproc/CPS1416-01
            # qq = ["data00", "data01"..]
            # Thus 'q' is succeeded data processing directory
            for q in qq:
                max_index = -9999
                # Data directory exists
                if q.rfind("data") != -1:
                    cols = q.split('/')
                    index_str = cols[-1].replace("data","")
                    #print int(index_str)
                    max_index = int(index_str)
                    #print max_index
                if max_index != -9999:
                    ddir_abs = os.path.abspath(abs_pin_dir)
                    #print ddir_abs
                    found_d = "%s/%s/" % (ddir_abs, q)
                    #print "EEEEE",found_d
                    self.found_procd.append(found_d)
                else:
                    if isDebug == True:
                        print "No data processed: %s" % q

        # Directories for 'each' data processing
        self.dir_dict["each_procd"] = self.found_procd

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

        self.dir_dict["small_wedge"] = self.multi_dirs
        self.dir_dict["large_wedge"] = self.largewedge_dirs

        print self.dir_dict

        if self.isDebug:
            for proc_type, dir in self.dir_dict.items():
                print "#########################################"
                print proc_type, dir
                print "#########################################"

        self.isPrep = True
        return self.found_procd

    def getTypeDirs(self, designated_key):
        if self.isPrep == False: self.prep()

        if designated_key not in self.dir_dict:
            raise MyException.NoKeysInDict("No designated key in the existing dict.")
        return self.dir_dict[designated_key]

    def getMergeDirs(self):
        if self.isPrep == False:
            self.prep()
        return self.merge_dirs

    def listupGoodProcesseDirs(self, type_of_data):
        if self.isPrep == False: self.prep()
        proc_dirs = self.getTypeDirs(type_of_data)

        # okay directories
        ok_dirs = []
        for proc_dir in proc_dirs:
            proc_files = glob.glob("%s/*"%os.path.abspath(proc_dir))
            for proc_file in proc_files:
                if proc_file.rfind("CORRECT.LP") != -1:
                    ok_dirs.append(proc_dir)

        return ok_dirs

    def listupBadProcessDirs(self, type_of_data):
        if self.isPrep == False: self.prep()

        proc_dirs = self.getTypeDirs(type_of_data)

        # NG directories
        ng_dirs = []
        for proc_dir in proc_dirs:
            isFound = False
            proc_files = glob.glob("%s/*"%os.path.abspath(proc_dir))
            for proc_file in proc_files:
                if proc_file.rfind("CORRECT.LP") != -1:
                    isFound = True
            # The process here failed.
            if isFound == False:
                ng_dirs.append(proc_dir)
        return ng_dirs

    # This is for each path directory
    def find_pin_datasets(self, proc_dir):
        cols = proc_dir.split('/')
        loop_index = 0
        for col in cols:
            if col.rfind("kamo") != -1:
                data_dir = os.path.join(cols[loop_index+1], cols[loop_index+2], cols[loop_index+3])
                return cols[loop_index+1], data_dir
            else:
                loop_index += 1

        MyException.NoKAMOpathInString("Designated columns do not include '_kamo*' path")

    # type_of_data: ["small_wedge", "large_wedge"]
    def analyzeProcessResults(self, type_of_data):
        if self.isPrep == False: self.prep()
        # good prodcess results
        good_proc_dirs = self.listupGoodProcesseDirs(type_of_data)
        bad_proc_dirs = self.listupBadProcessDirs(type_of_data)


        # Good proc dirs
        for good_proc_dir in good_proc_dirs:
            try:
                pin_dir, data_dir = self.find_pin_datasets(good_proc_dir)
                kamo_decision_str = self.checkKAMOdecision(good_proc_dir)
                proc_info = pin_dir, data_dir, kamo_decision_str, good_proc_dir
                print proc_info
            except Exception as e:
                print e.args

        for bad_proc_dir in bad_proc_dirs:
            try:
                pin_dir, data_dir = self.find_pin_datasets(bad_proc_dir)
                kamo_decision_str = self.checkKAMOdecision(bad_proc_dir)
                proc_info = pin_dir, data_dir, kamo_decision_str, bad_proc_dir
                print proc_info

            except Exception as e:
                print e.args

    
    def checkKAMOdecision(self, proc_path):
        check_file = "%s/decision.log" % proc_path
        lines = open(check_file,"r").readlines()
        error_message = "Normally processed"
        for line in lines:
            if line.rfind("error:") != -1:
                error_message = line.replace("error:","").strip()
            if line.rfind("failed") != -1:
                error_message = line.strip()

        return error_message

    def getMultiDirs(self):
        if self.isPrep == False:
            self.prep()
        return self.multi_dirs

    def getGoodLargeWedgeDirs(self):
        if self.isPrep == False:
            self.prep()

        #print "MULTI NDS = ", len(self.multi_dirs)
        print "LARGE NDS = ", len(self.largewedge_dirs)
        #print "MERGE DIR = ", len(self.merge_dirs)

        # CORRECT.LP existing data processing paths.
        success_paths, bad_paths = self.evaluate_largewedge(self.largewedge_dirs)

        return success_paths

if __name__ == "__main__":
    arc_files = []
    jw = AnalyzeDirInKAMO(sys.argv[1])

    #small_wedge_okay = jw.listupGoodProcesseDirs("small_wedge")
    #ng_dirs = jw.listupBadProcessDirs("small_wedge")
    #print small_wedge_okay
    #print "NG=", ng_dirs

    jw.analyzeProcessResults("small_wedge")
    jw.analyzeProcessResults("large_wedge")


    """
    success_paths = jw.getGoodLargeWedgeDirs()
    print ("success_path=", success_paths)
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
    """

    #print arc_command
    #os.system(arc_command)
