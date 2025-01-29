import sys,os
sys.path.append("/isilon/BL32XU/BLsoft/PPPP/")
sys.path.append("/isilon/BL32XU/BLsoft/PPPP/11.ClusterAnalysis/")
import glob,numpy
import DirectoryProc

# Input file for path list to be searched.
path_file = sys.argv[1]
lines = open(path_file, "r").readlines()

# Check paths as 'absolute' paths
abs_paths = []
for line in lines:
    abs_path = os.path.abspath(line).strip()
    abs_paths.append(abs_path)

okay_dirs = []

for check_path in abs_paths:
    # Finding 'final' directories in designated paths
    print "Searching %s"  % check_path
    dp=DirectoryProc.DirectoryProc(check_path)
    dirs=dp.findTargetDirs("final")

    if len(dirs) == 0:
        print "Skipping ", check_path
        continue

    print "dirs=", dirs
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
        print "Skipping ", check_path
        continue

    max_cluster_d=maxd.split("run_")[0]
    print "Checking %s" % max_cluster_d
    dp=DirectoryProc.DirectoryProc(max_cluster_d)

    rundirs= dp.findTargetDirs("run")

    run_max=0
    for rund in rundirs:
        run_no=int(rund.split("run")[1].split("/")[0].replace("_",""))
        if run_no > run_max:
            run_max=run_no
            final_d=rund
    ccp4_mtz_path = os.path.join(final_d,"ccp4/xscale.mtz")
    okay_dirs.append(ccp4_mtz_path)

outfile = open("xscale.lst", "w")

for fpath in okay_dirs:
    outfile.write("%s\n" % fpath)

outfile.close()

#print okay_dirs
"""
    command1="pwd > %s/file_location.txt"%final_d
    dd=final_d
    command2="tar cvfz %s/%s.tgz %s/XSCALE.INP %s/aniso.log %s/XSCALE.LP %s/ccp4/"%(store_path,prefix,dd,dd,dd,dd)

print command1
print command2
os.system(command1)
os.system(command2)
"""
###
