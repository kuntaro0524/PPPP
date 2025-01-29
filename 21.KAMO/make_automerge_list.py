import os,sys,math,glob
import time
sys.path.append("/isilon/BL32XU/BLsoft/PPPP")
import DirectoryProc

if __name__ == "__main__":
    dp=DirectoryProc.DirectoryProc(sys.argv[1])
    dlist=dp.getDirList()

    merge_title="merge_all.csv"
    data_name="ligand"
    anomalous="no"
    cell_dimensions="132 172 68 90 90 90"
    space_group="P21212"

    ofile=open("merge_all.csv","w")

    dlist.sort()
    for d in dlist:
        ofile.write("%s,%s,%s,%s\n"%(d,data_name,cell_dimensions,space_group))
