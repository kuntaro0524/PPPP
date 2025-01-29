import sys,os
import h5py
from yamtbx.dataproc import eiger
from yamtbx.dataproc import cbf
from yamtbx.dataproc.XIO.plugins import eiger_hdf5_interpreter
from libtbx import easy_mp
import glob
import HD5CBF

if __name__=="__main__":
        lines=open(sys.argv[1],"r").readlines()
        conds_list=[]
	mpmp=HD5CBF.HD5CBF()

	root_dir="."

	print type(lines)
	image_index=100


        for line in lines:
		master_file=line.strip()
		prefix=master_file[master_file.rfind("/")+1:master_file.rfind("_master")]
		print "PREFIX",prefix
                startnum=image_index
                endnum=image_index
                cbf_dir="%s/%s/"%(root_dir,prefix)
        
                if os.path.exists(cbf_dir)==False:
                        os.mkdir(cbf_dir)

                cbfile="%s/head-%d.cbf"%(cbf_dir,image_index)
        
                compo=master_file,startnum,endnum,cbfile
                conds_list.append(compo)

	print "#######################"
	print conds_list[0]
	print "#######################"

        easy_mp.pool_map(fixed_func=lambda n: mpmp.merge(n), args=conds_list, processes=8)
