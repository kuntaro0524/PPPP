import sys,os
sys.path.append("/isilon/BL32XU/BLsoft/PPPP/")
sys.path.append("/isilon/BL32XU/BLsoft/PPPP/11.ClusterAnalysis/")
import glob,numpy
import DirectoryProc

# STORAGE .tgz path
store_path="/isilon/BL32XU/TMP/"
prefix=os.environ["PWD"].split("/")[-1]

# Finding xscale.mtz
dp=DirectoryProc.DirectoryProc(os.environ["PWD"])

dirs=dp.findTargetDirs("final")

max_cluster_no=0
for d in dirs:
    if d.rfind("run_")!=-1:
        cluster_no=int(d.split("cluster")[1].replace("_","").split("/")[0])
        if cluster_no > max_cluster_no:
            max_cluster_no=cluster_no
            maxd=d

max_cluster_d=maxd.split("run_")[0]
dp=DirectoryProc.DirectoryProc(max_cluster_d)

rundirs= dp.findTargetDirs("run")

run_max=0
for run in rundirs:
    run_no=int(run.split("run")[1].split("/")[0].replace("_",""))
    if run_no > run_max:
        run_max=run_no
        final_d=run

command1="pwd > %s/file_location.txt"%final_d
dd=final_d
command2="tar cvfz %s/%s.tgz %s/XSCALE.INP %s/aniso.log %s/XSCALE.LP %s/ccp4/"%(store_path,prefix,dd,dd,dd,dd)

print command1
print command2

os.system(command1)
os.system(command2)
