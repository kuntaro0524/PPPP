import os,sys,math,glob
import time
sys.path.append("/isilon/BL32XU/BLsoft/PPPP/")
import DirectoryProc

if __name__ == "__main__":
	dp=DirectoryProc.DirectoryProc(sys.argv[1])
	dlist=dp.getDirList()

	for dire in dlist:
		abs_path=os.path.abspath(dire)
		targetlist=dp.findTarget("XDS_ASCII.HKL")

	# Sort
	targetlist.sort()
	curr_dir=os.path.abspath(".")

	comindex=0
	list_file=open("mtz.lst","w")
	for tfile in targetlist:
		tpath=tfile.replace("XDS_ASCII.HKL","")
		comname="com_%05d.com"%comindex
		comf=open(comname,"w")
		print "COMFILE"
		comf.write("#!/bin/csh\n")
		comf.write("#$ -cwd\n")
		comf.write("cd %s\n"%tpath)
		comf.write("xds2mtz.py --add-test-flag --space-group=P212121\n")
		comf.close()
		os.system("chmod 744 ./%s"%comname)
		time.sleep(1.0)
		print "QSUB"
		os.system("qsub ./%s"%comname)
		#com="xds2mtz.py --add-test-flag --space-group=P212121"
		list_file.write("%s"%tpath)
		comindex+=1
