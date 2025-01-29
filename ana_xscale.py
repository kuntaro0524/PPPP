import os
import DirectoryProc
import AnaCORRECT

dp=DirectoryProc.DirectoryProc("./")

targetname="XSCALE.LP"
logfile=targetname.replace("LP","csv")
ofile=open(logfile,"w")

lll=dp.findTarget(targetname)
lll.sort()

curr_dir=os.path.abspath("./")

for l in lll:
	ac=AnaCORRECT.AnaCORRECT(l)
	ofile.write("# %s\n"%curr_dir)
	for logstr in ac.readLog():
		ofile.write("%s"%logstr)
	ofile.write("\n\n")
