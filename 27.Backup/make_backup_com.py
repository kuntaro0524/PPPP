import os, sys, math
sys.path.append("/isilon/BL32XU/BLsoft/PPPP/Libs/")

import MyDate

# read directory list for backup
lines = open(sys.argv[1], "r").readlines()

# HDD path
hdd_path = sys.argv[2]

# HDD check
if os.path.exists(hdd_path):
    if os.access(hdd_path, os.W_OK):
        print "Writing files to %s" % hdd_path
    else:
        print "Please check HDD writing permission"
else:
    print "Please input 'existing' path... %s" % hdd_path

cwd = os.getcwd()

# Com file name
mydate = MyDate.MyDate()
comname = "backup_%s.com" % mydate.getNowMyFormat("min")
comfile = open(comname, "w")

for line in lines:
    path_in_file = line.strip()
    rel_path = os.path.relpath(path_in_file, cwd)

    # HDD directory
    each_dir_on_hdd = os.path.join(hdd_path, rel_path)
    if os.path.exists(each_dir_on_hdd) == False:
        print "making directory:%s" % each_dir_on_hdd
        os.makedirs(each_dir_on_hdd)
    else:
        print "%s already exists" % each_dir_on_hdd

    # backup string
    comfile.write("rsync -auv %s/ %s/\n" % (rel_path, each_dir_on_hdd))