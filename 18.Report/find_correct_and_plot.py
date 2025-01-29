import os,sys,math,glob
import time
sys.path.append("/isilon/BL32XU/BLsoft/PPPP/")
import DirectoryProc

if __name__ == "__main__":
	dp=DirectoryProc.DirectoryProc(sys.argv[1])
	dlist=dp.getDirList()

	import AnaCORRECT
	for dire in dlist:
		abs_path=os.path.abspath(dire)
		targetlist=dp.findTarget("CORRECT.LP")

	# Sort
	targetlist.sort()

	ofile=open("correct_lp.dat","aw")
	#print targetlist
	for tfile in targetlist:
		print "Processing %s"%tfile
		ac=AnaCORRECT.AnaCORRECT(tfile)
		logstr=ac.readLog()

		ofile.write("## %s ##\n"%tfile)
		for log in logstr:
			ofile.write("%s"%log)
		ofile.write("\n\n")
