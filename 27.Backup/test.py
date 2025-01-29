import os,sys
sys.path.append("/isilon/BL32XU/BLsoft/PPPP/")
import DirectoryProc

def get_size(start_path = '.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

dp = DirectoryProc.DirectoryProc("./")
dirlist = dp.getDirList()

hdd_size_TB = 8.0

dir_size_array = []
total_size = 0.0

for d in dirlist:
    if os.access(d,os.R_OK):
        try:
            size_tmp = get_size(d)
            size_mb = size_tmp/1E6
            size_gb = size_mb/1000.0
            print "%s %8.3f GB"%(d,size_gb)
            dir_size_array.append((d, size_gb))
            total_size += size_tmp
        except:
            print "Failed to get size"
            continue

n_dir = len(dir_size_array)
total_size_TB = size_gb / 1000.0

if total_size_TB > hdd_size_TB:
    print "Arranging directory list is required"

ofile = open("dire_size.lst","w")
for d, size_gb in dir_size_array:
    ofile.write("%50s,%8.3f\n"%( d,size_gb))
