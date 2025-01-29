import sys,os,math,numpy
import ConvertHD5
import h5py,glob
from libtbx import easy_mp

if len(sys.argv)!=3:
    print "Usage: PROG MASTER_FILE NDATASETS OUTDIR"

master_file=sys.argv[1]
ndata=int(sys.argv[2])
outdir=sys.argv[3]
nframes_data=100
n_sumup=10

if os.path.exists(outdir)==False:
    os.makedirs(outdir)
    outpath=os.path.abspath(outdir)

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
