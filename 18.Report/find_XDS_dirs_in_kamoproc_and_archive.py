import sys, os, numpy, time
os.sys.path.append("/isilon/BL32XU/BLsoft/PPPP/")
import DirectoryProc
import MyDate

# Check paths as 'absolute' paths
abs_paths = []

lines = open(sys.argv[1], "r").readlines()
for line in lines:
    abs_path = os.path.abspath(line).strip()
    abs_paths.append(abs_path)

okay_dirs = []

da = MyDate.MyDate()
dstr = da.getNowMyFormat(option="other")

file_prefix = sys.argv[2]
arc_name = "%s_%s_XDSresults.tgz" % (dstr, file_prefix)
command = "tar cvfz %s " % arc_name

arcpaths = []
for check_path in abs_paths:
    # Finding 'final' directories in designated paths
    dp=DirectoryProc.DirectoryProc(check_path)
    filepaths, xdspaths = dp.findTargetFileInTargetDirectories("_kamoproc","CORRECT.LP",exclude_str="")
    idx = 0

    arcpaths.append(xdspaths[0])
    tpath = xdspaths[0]

    for filename in ["XDS_ASCII.HKL","CORRECT.LP"]:
        tfname =  "%s/%s" % (tpath, filename)
        if os.path.exists(tfname):
            #print tfname
            relpath = os.path.relpath(tfname)
            command += "%s " % relpath

# Making archive for sending
os.system(command)
mv_com = "cp -f %s /isilon/BL32XU/TMP/" % arc_name
os.system(mv_com)
check_com = "du -hs /isilon/BL32XU/TMP/%s" % arc_name
time.sleep(10.0)
os.system(check_com)
