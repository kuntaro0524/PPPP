import os,sys,math,numpy
sys.path.append("/isilon/BL32XU/BLsoft/PPPP/")
import DirectoryProc

dp = DirectoryProc.DirectoryProc("./")
dlist = dp.getDirList()

dlist.sort()

#/isilon/users/target/target/AutoUsers/190122/Toma/_kamoproc/KOZO0004-01,apo,no,132 172 68 90 90 90,P21212

ofile = open("template.csv","w")
for d in dlist:
    ofile.write("%s,%s,no\n"%(d,sys.argv[1]))

ofile.close()
