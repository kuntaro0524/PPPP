import sys,os,subprocess
sys.path.append("/isilon/BL32XU/BLsoft/PPPP/")
import glob,numpy
import DirectoryProc
import AnaCORRECT

def exec_cmd(cmd):
  return subprocess.Popen(
      cmd, stdout=subprocess.PIPE,
      shell=True).communicate()[0]

# Finding xscale.mtz
reflection_file = sys.argv[1]
dp=DirectoryProc.DirectoryProc(os.environ["PWD"])
xscalehkl_list,path_list=dp.findTarget(reflection_file)

# Log file
logf=open("xdsascii_resol.dat","w")

for xscalehkl in xscalehkl_list:
    command = "yamtbx.python /oys/xtal/yamtbx/yamtbx/dataproc/auto/command_line/decide_resolution_cutoff.py %s"%xscalehkl
    logs = exec_cmd(command)
    lines = logs.split('\n')

    for line in lines:
        if line.rfind("Suggested cutoff")!=-1:
            resolution = float(line.split()[2])
            logf.write("%s %5.2f\n"%(xscalehkl, resolution))

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
easy_mp.pool_map(fixed_func=lambda n: ConvertHD5.ConvertHD5(n).process(), args=proc_list, processes=12)
"""
