import sys, os, numpy
os.sys.path.append("/isilon/BL32XU/BLsoft/PPPP/")
import DirectoryProc

# Check paths as 'absolute' paths
abs_paths = []

if len(sys.argv) ==2:
    lines = open(sys.argv[1], "r").readlines()
    for line in lines:
        abs_path = os.path.abspath(line).strip()
        abs_paths.append(abs_path)
else:
    abs_path = os.path.abspath("./").strip()
    abs_paths.append(abs_path)

okay_dirs = []

# findTargetFileInTargetDirectories(self,string_in_dire,string_in_filename,exclude_str=""):

arc_name = "arc.tgz"
command = "tar cvfz %s " % arc_name

print abs_paths

arcpaths = []
for check_path in abs_paths:
    # Finding 'final' directories in designated paths
    print check_path
    dp=DirectoryProc.DirectoryProc(check_path)
    filepaths, xdspaths = dp.findTargetFileInTargetDirectories("_kamoproc","CORRECT.LP",exclude_str="")
    idx = 0

    arcpaths.append(xdspaths[0])
    tpath = xdspaths[0]

    for filename in ["XDS_ASCII.HKL","CORRECT.LP"]:
        tfname =  "%s/%s" % (tpath, filename)
        if os.path.exists(tfname):
            print tfname
            relpath = os.path.relpath(tfname)
            command += "%s " % relpath
