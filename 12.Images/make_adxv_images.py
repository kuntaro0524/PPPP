import sys,os

lines=open(sys.argv[1],"r").readlines()

score_min=10000
score_max=50000

for line in lines:
	cols=line.split()
	#print cols
	xds_ascii_file=cols[0]
	score=float(cols[1])

	if score > score_min and score < score_max:
		passes=xds_ascii_file.split('/')
		#print passes
		rootpath="%s/%s/cbf/"%(passes[0],passes[1])
		fname=passes[2]
		#print fname
		mmm=fname.split("_")
		#print mmm
		prefix=mmm[0]
		nums=mmm[1].split("-")
		start=int(nums[0])
		end=int(nums[1])
		mid=int((start+end)/2.0)
		sn=mid-5
		en=mid+5
		cbfname="%s/merged-%d-%d.cbf"%(rootpath,sn,en)
		print "adxv %s"%cbfname
