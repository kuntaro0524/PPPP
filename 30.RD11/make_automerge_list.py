import os,sys,math,glob
import time
sys.path.append("/isilon/BL32XU/BLsoft/PPPP")
import DirectoryProc

if __name__ == "__main__":
    dp=DirectoryProc.DirectoryProc(sys.argv[1])
    dlist=dp.getDirList()

    #print dlist

    ofile = open("data_proc.csv", "w")

    dose_list = ["05MGy","10MGy","15MGy","20MGy"]
    dose_valu = [5,10,15,20]

    ofile.write("topdir,name,anomalous\n")
    for d in dlist:
        for i, dose_str in enumerate(dose_list):
            #print dose_str
            if d.rfind(dose_str) != -1:
                ofile.write("%s,%s,%s\n" % (d,dose_str,"yes"))

    ofile.close()
