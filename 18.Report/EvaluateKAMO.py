import sys,os
sys.path.append("/isilon/BL45XU/BLsoft/PPPP/")
sys.path.append("/isilon/BL45XU/BLsoft/PPPP/11.ClusterAnalysis/")
sys.path.append("/isilon/BL45XU/BLsoft/PPPP/18.Report/")

import glob,numpy
import DirectoryProc
import MyDate
import time
import XSCALEReporter

#########################################
def evaluate_largewedge(dires):
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

    #print ok_paths
    return ok_paths, bad_paths
    
#########################################

# DEBUG flag
isDebug = False
isIncludeMTZ = False

# directories where merge was proceeded.
dp = DirectoryProc.DirectoryProc(".")
dd = dp.findDirs()


# Finding data processing directory
found_procd = []
for data_dir in dd:
    pp = DirectoryProc.DirectoryProc(data_dir)
    qq = pp.findDirs()
    for q in qq:
        max_index = -9999
        if q.rfind("data") != -1:
            cols = q.split('/')
            index_str = cols[-1].replace("data","")
            #print int(index_str)
            max_index = int(index_str)
            #print max_index
            #print mpath
        if max_index != -9999:
            ddir_abs = os.path.abspath(data_dir)
            #print ddir_abs
            found_d = "%s/%s/" % (ddir_abs, q)
            #print "EEEEE",found_d
            found_procd.append(found_d)
        else:
            print "No data processed: %s" % q

multi_dirs = []
largewedge_dirs = []
for procd_abs in found_procd:
    ddd = DirectoryProc.DirectoryProc(procd_abs)
    procd_dirs = ddd.findDirs()
    
    for procd in procd_dirs:
        if procd.rfind("multi") != -1:
            final_path = os.path.join(procd_abs, procd)
            multi_dirs.append(final_path)
        else:
            final_path = os.path.join(procd_abs, procd)
            largewedge_dirs.append(final_path)

print "MULTI NDS = ", len(multi_dirs)
print "LARGE NDS = ", len(largewedge_dirs)

# CORRECT.LP existing data processing paths.
success_paths, bad_paths = evaluate_largewedge(largewedge_dirs)

arc_files = []
required_files = ["CORRECT.LP", "XDS_ASCII.HKL"]
arc_command = "tar cvfz ttttt.tgz "
for ok in success_paths:
    for required_file in required_files:
        file_path = os.path.join(ok, required_file)
        if os.path.exists(file_path) == True:
            rel_path = os.path.relpath(file_path, "./")
            print "RRRRR=",rel_path
            arc_files.append(rel_path)
            arc_command += "%s " % rel_path

print arc_command
os.system(arc_command)
