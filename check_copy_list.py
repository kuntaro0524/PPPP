import os,sys,math
import filecmp
from yamtbx.dataproc import eiger
from yamtbx.dataproc import cbf
from yamtbx.dataproc.XIO.plugins import eiger_hdf5_interpreter
from libtbx import easy_mp


#filecmp.dircmp('example/dir1', 'example/dir2').report()


# ISILON root directory
isilon_root=sys.argv[1]

# Raw image root directory
back_root=sys.argv[2]

print "   HDD path: %s"%back_root
print "ISILON path: %s"%isilon_root

#fcmp=filecmp.dircmp(isilon_root,back_root).report()
fcmp=filecmp.dircmp(isilon_root,back_root)

isilon_dirs=fcmp.left_list
hdd_dirs=fcmp.right_list
common_dirs=fcmp.common

# DEF
def get_size(targetpath):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(targetpath):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return float(total_size/1E9)

def check_func(comppaths):
    left_path,right_path=comppaths
    left_size=get_size(left_path)
    right_size=get_size(right_path)

    diff_size=math.fabs(left_size-right_size)

    if diff_size > 1.0:
        print "Not yet %s"%isilon_path

comppaths=[]

for comdir in common_dirs:
	isilon_path="%s/%s/"%(isilon_root,comdir)
	back_dir="%s/%s/"%(back_root,comdir)
	comppaths.append((isilon_path,back_dir))

for not_copy in isilon_dirs:
	print "not copied: %s"%not_copy

easy_mp.pool_map(fixed_func=lambda n: check_func(n), args=comppaths, processes=8)
