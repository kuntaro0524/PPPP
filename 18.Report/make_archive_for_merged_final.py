import sys,os
sys.path.append("/isilon/BL32XU/BLsoft/PPPP/")
sys.path.append("/isilon/BL32XU/BLsoft/PPPP/11.ClusterAnalysis/")
import glob,numpy
import DirectoryProc
import MyDate
import XSCALEReporter
# DEBUG flag
isDebug = False

# Input file for path list to be searched.
path_file = sys.argv[1]
prefix = sys.argv[2]
lines = open(path_file, "r").readlines()

# Check paths as 'absolute' paths
abs_paths = []
for line in lines:
    abs_path = os.path.abspath(line).strip()
    abs_paths.append(abs_path)

okay_dirs = []
data_roots = []

for check_path in abs_paths:
    # Finding 'final' directories in designated paths
    #print "Searching %s"  % check_path
    dp=DirectoryProc.DirectoryProc(check_path)
    dirs=dp.findTargetDirs("final")

    if len(dirs) == 0:
        if isDebug: print "Skipping ", check_path
        continue

    #print "dirs=", dirs
    max_cluster_no=0
    maxd = -9999
    for d in dirs:
        if d.rfind("run_")!=-1:
            #print "checking %s" % d
            cluster_no=int(d.split("cluster")[1].replace("_","").split("/")[0])
            if cluster_no > max_cluster_no:
                max_cluster_no=cluster_no
                maxd=d

    if maxd == -9999:
        #print "Skipping ", check_path
        continue

    max_cluster_d=maxd.split("run_")[0]
    #print "Checking %s" % max_cluster_d
    dp=DirectoryProc.DirectoryProc(max_cluster_d)

    rundirs= dp.findTargetDirs("run")

    run_max=0
    for rund in rundirs:
        run_no=int(rund.split("run")[1].split("/")[0].replace("_",""))
        if run_no > run_max:
            run_max=run_no
            final_d=rund

    #ccp4_mtz_path = os.path.join(final_d,"ccp4/xscale.mtz")
    #if os.path.exists(ccp4_mtz_path) == True:
    #    okay_dirs.append(ccp4_mtz_path)

    #print "FINALD=", final_d
    if len(data_roots) == 0:
        data_roots.append(final_d)
    else:
        if isDebug:
            print "<<<<<"
            print data_roots
            print ">>>>>"
        for data_root in data_roots:
            if isDebug:
                print "####################"
                print "COMPARE(fin   )=", final_d
                print "COMPARE(Stored)=", data_root
            if final_d == data_root:
                if isDebug: print "Identical!!!"
                continue
            if isDebug: print "STORED:", final_d
            data_roots.append(final_d)
            break

if isDebug:
    for d in data_roots:
        print "DDD=", d

check_list = ["XSCALE.LP", "XSCALE.INP", "aniso.log", "pointless.log"]

all_list = []
saved_dir = ""
xscale_list = []
for data_root in data_roots:
    if isDebug: print "D=", data_root
    if saved_dir == data_root:
        if isDebug: print "IDENTICAL!!!!"
        continue
    else:
        saved_dir = data_root

    for check_file in check_list:
        check_path = os.path.join(data_root, check_file)
        if os.path.exists(check_path) == True:
            relpath = os.path.relpath(check_path)
            all_list.append(relpath)
            if relpath.rfind("XSCALE.LP") != -1:
                xscale_list.append(data_root)
    # MTZ file
    mtz_path = os.path.join(data_root, "ccp4/xscale.mtz")
    mtz_relpath = os.path.relpath(mtz_path)
    all_list.append(mtz_relpath)

# Making XSCALE results
#reporter = XSCALEReporter.XSCALEReporter(xscale_path)
#reporter.makeHTML(figdpi=65)

# Making archive commend
da = MyDate.MyDate()
dstr = da.getNowMyFormat(option="other")

command = "tar cvfz %s_%s.tgz " % (dstr, prefix)
for good_file in all_list:
    if isDebug: print "GOOD",good_file
    command += "%s " % good_file

print "COMMAND=",command
os.system(command)

#command1="pwd > ./file_location.txt"
#command2="tar cvfz ./%s_%s.tgz %s/XSCALE.INP %s/aniso.log %s/XSCALE.LP %s/ccp4/"%(dstr,prefix,dd,dd,dd,dd)
#os.system(command1)
#os.system(command2)
