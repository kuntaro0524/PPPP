import sys,os
sys.path.append("/isilon/BL32XU/BLsoft/PPPP/")
sys.path.append("/isilon/BL32XU/BLsoft/PPPP/11.ClusterAnalysis/")
import glob,numpy
import DirectoryProc
import sys,os,subprocess
import AnaCORRECT
from libtbx import easy_mp

class MakeReportKAMO:
    def __init__(self, root_path, out_dir):
        self.root_path = os.path.abspath(root_path)
        self.tgz_path = "./"
        # STORAGE .tgz path
        self.store_path= os.path.abspath(out_dir)
        self.pwd=os.environ["PWD"]
        self.isFind = False
        self.isPrep = False

    def prepOutDir(self):
        if os.path.exists(self.store_path):
            print "Directory is ready"
        else:
            os.makedirs(self.store_path)
        self.isPrep = True

    def getRunNumber(self, dirname):
        cols = dirname.split('/')
        #print cols
        for col in cols:
            if col.rfind("run_") != -1:
                return int(col.replace("run_",""))

    def findClusters(self, ncluster=3):
        # Finding xscale.mtz
        dp=DirectoryProc.DirectoryProc(self.root_path)
        dirs=dp.findTargetDirs("final")

        self.possible_clusters = []
        max_cluster_no=0
        for d in dirs:
            # exclude ccp4/ path
            if d.rfind("ccp4") != -1:
                continue
            if d.rfind("run_")!=-1:
                cluster_no=int(d.split("cluster")[1].replace("_","").split("/")[0])
                run_num = self.getRunNumber(d)
                if run_num != 3:
                    continue
                self.possible_clusters.append((cluster_no,d))

        self.possible_clusters.sort(key=lambda x:x[0], reverse=True)
        self.final_clusters = []
        for i in range(0,3):
            self.final_clusters.append(self.possible_clusters[i])
        self.isFind = True

    def makeTarBall(self):
        if self.isFind == False:
            self.findClusters()
        if self.isPrep == False:
            self.prepOutDir()

        arc_list = ""
        for cluster_no, final_dir in self.final_clusters:
            #print cluster_no, final_dir
            rp = os.path.relpath(final_dir, self.pwd)
            #print rp
            arc_list += "%s/xscale.hkl %s/XSCALE.INP %s/aniso.log %s/pointless.log %s/XSCALE.LP %s/ccp4/ "%(rp, rp, rp, rp, rp, rp)

        #print arc_list
        prefix=os.environ["PWD"].split("/")[-1]
        #print prefix
        command1="pwd > ./file_location.txt"
        os.system(command1)
        command2="tar cvfz %s/%s.tgz %s ./file_location.txt cells.dat formerge.lst"%(self.store_path,prefix,arc_list)
        #print command2
        os.system(command2)

    def calcResolLimit(self, refl_file):
        command = "yamtbx.python /oys/xtal/yamtbx/yamtbx/dataproc/auto/command_line/decide_resolution_cutoff.py %s"%refl_file
        logs = subprocess.Popen(command, stdout=subprocess.PIPE,shell=True).communicate()[0]
        lines = logs.split('\n')
        for line in lines:
            if line.rfind("Suggested cutoff")!=-1:
                resolution = float(line.split()[2])
                self.logf.write("%s %5.2f\n"%(refl_file, resolution))
                return refl_file, resolution

    def makeResolutionListFrom(self, reflection_name):
        # Finding xscale.mtz
        abs_path=os.path.abspath(self.root_path)
        dp=DirectoryProc.DirectoryProc(abs_path)
        reffile_list,path_list=dp.findTarget(reflection_name)

        # Log file
        self.logf=open("resol.dat","w")
        easy_mp.pool_map(fixed_func=lambda n: self.calcResolLimit(n), args=reffile_list, processes=8)
        
"""
proc_list=[]
for i in numpy.arange(0,ndata):
    nframes_data/2.0
    sum_start_num=i*nframes_data+int(nframes_data/2.0)-int(n_sumup/2.0)+1
    sum_end_num=sum_start_num+n_sumup-1

    start_num=i*nframes_data+1
    end_num=start_num+nframes_data-1
    print start_num,end_num

    outfile="%s/multi_%d-%d.cbf"%(outpath,start_num,end_num)
    print outfile
    proc_list.append((master_file,sum_start_num,sum_end_num,outfile))

print "making %05d files"%len(proc_list)
"""

if __name__ == "__main__":
    kamorepo = MakeReportKAMO(sys.argv[1], sys.argv[2])
    #kamorepo.makeTarBall()
    #kamorepo.makeTarBall()
    kamorepo.makeResolutionListFrom("XDS_ASCII.HKL")
