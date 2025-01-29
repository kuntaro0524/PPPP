import os,sys,math,glob
import time
import DirectoryProc

if __name__ == "__main__":
	dp=DirectoryProc.DirectoryProc(sys.argv[1])
	dlist=dp.getDirs()

	import AnaCORRECT
	for dire in dlist:
		abs_path=os.path.abspath(dire)
		targetlist=dp.findTarget("CORRECT_fullres.LP")

	# Get data name
	relative_bsslog_path="../../"
	bsslog_searchname="ds01.log"
	dname=abs_path.split('/')[-2]
	bsslogpath="%s/%s/%s/data/%s"%(abs_path,relative_bsslog_path,dname,bsslog_searchname)

	# Sort
	targetlist.sort()

	ofile=open("correct_lp.dat","w")
	for tfile in targetlist:
		ac=AnaCORRECT.AnaCORRECT(tfile)
		logstr=ac.read()

		ofile.write("## %s ##\n"%tfile)
		for log in logstr:
			ofile.write("%s"%log)
		ofile.write("\n\n")
