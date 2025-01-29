import os,sys,math


lines=open(sys.argv[1]).readlines()
r_thresh=float(sys.argv[2])

line_idx=0
for line in lines:
	if line.rfind("R-FACTORS FOR INTENSITIES OF DATA SET")!=-1:
		cols=line.split()
		line2=lines[line_idx+5]
		cols2=line2.split()
		rfac=float(cols2[1].replace("%",""))
		fname=cols[6]
		if rfac <= r_thresh:
			print "INPUT_FILE=%s"%fname
#lines[line_idx+5]
	line_idx+=1
