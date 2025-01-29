import os, sys, math
sys.path.append("/isilon/BL32XU/BLsoft/PPPP/")
import DirectoryProc

keywords = ["cry"]

dp = DirectoryProc.DirectoryProc("./")

dlist = dp.findDirsWithName(keywords[0])
dlist.sort()

ofile = open("automerge.csv", "w")
# Header
ofile.write("topdir,name,anomalous\n")

for each_dir in dlist:
    data_name = each_dir.split("_")[1]
    cry_index, dose_index = data_name.split("-")
    dose_index = int(dose_index)
    dose_amount = 1.0 * float(dose_index)

    abspath = os.path.abspath(each_dir)
    dose_label = "%dMGy" % int(dose_amount)
    ofile.write("%s, %s, no\n" % (abspath, dose_label))

ofile.close()
