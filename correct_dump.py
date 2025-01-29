import os,sys
import AnaCORRECT

infile=sys.argv[1]
outfile=sys.argv[2]

ofile=open(outfile,"w")

ac=AnaCORRECT.AnaCORRECT(infile)
ofile.write("# %s\n"%infile)

for logstr in ac.readLog():
	ofile.write("%s"%logstr)
