import sys,os,subprocess
sys.path.append("/isilon/BL32XU/BLsoft/PPPP/")
import glob,numpy
import DirectoryProc
import AnaCORRECT

from yamtbx.dataproc import eiger
from yamtbx.dataproc import cbf
from yamtbx.dataproc.XIO.plugins import eiger_hdf5_interpreter
from libtbx import easy_mp


def exec_cmd(cmd):
  return subprocess.Popen(
      cmd, stdout=subprocess.PIPE,
      shell=True).communicate()[0]

# Finding xscale.mtz
reflection_file = sys.argv[1]
dp=DirectoryProc.DirectoryProc(os.environ["PWD"])
xscalehkl_list,path_list=dp.findTarget(reflection_file)

# Log file
logf=open("xscale_resol.dat","w")

def calc_resolution_limit(xds_outlog):
    command = "yamtbx.python /oys/xtal/yamtbx/yamtbx/dataproc/auto/command_line/decide_resolution_cutoff.py %s"% xds_outlog
    print "command=",command
    logs = exec_cmd(command)
    lines = logs.split('\n')

    for line in lines:
        if line.rfind("Suggested cutoff")!=-1:
            try:
                resolution = float(line.split()[2])
                print "Suggested cutoff=", resolution
                return xds_outlog, resolution
            except:
                return xds_outlog,-999.999

list_answers = easy_mp.pool_map(fixed_func=lambda n: calc_resolution_limit(n), args=xscalehkl_list, processes=16)

print list_answers

for compo in list_answers:
    if compo == None:
        continue
    print "COMPO=",compo

    filename, resolution = compo
    logf.write("%20s %5.2f\n" % (filename, resolution))

    print "WRITTEN"

logf.close()

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
