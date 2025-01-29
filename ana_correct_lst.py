import os,sys
import DirectoryProc
import AnaCORRECT

lstfile=sys.argv[1]
filelist=open(lstfile,"r").readlines()

ofile=open("dum","a")

file_index=0
for eachname in filelist:
	ofile=open("correct%02d.csv"%file_index,"w")
	filepath=os.path.abspath(eachname).strip()
	ac=AnaCORRECT.AnaCORRECT(filepath)
	ofile.write("# %s\n"%filepath)
	for logstr in ac.readLog():
		ofile.write("%s"%logstr)
	file_index+=1
