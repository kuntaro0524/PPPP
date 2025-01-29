import sys,os,math

lines=open(sys.argv[1],"r").readlines()

prefix=sys.argv[1].replace(".lst","")
n_line=len(lines)
n_div=1000

n_file=0

for n in range(0,n_line):
	if n%n_div==0:
		oname="%s_%03d.lst"%(prefix,n_file)
		cname="%s_%03d.com"%(prefix,n_file)
		ofile=open(oname,"w")
		cfile=open(cname,"w")
		cfile.write("#!/bin/csh\n")
		cfile.write("#$ -cwd\n")
		cfile.write("kamo.resolve_indexing_ambiguity nproc=8 ")
		cfile.write("method=reference ")
		cfile.write("reference_file=/isilon/BL32XU/BLsoft/PPPP/16.ManyMerge/ph.mtz ")
		cfile.write("./%s\n"%oname)
		cfile.close()
		os.system("chmod a+rx ./%s"%cname)
		os.system("qsub %s"%cname)
		n_file+=1
	ofile.write("%s"%lines[n])
