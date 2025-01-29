import sys,os,math

infile=open(sys.argv[1],"r")
lines=infile.readlines()
infile.close()

# Shutter open voltage ~3.4V

skip_head=10

oname=sys.argv[1].replace(".csv","_conv.dat")
ofile=open(oname,"w")

print "Converting %s to %s"%(sys.argv[1],oname)

idx=0
for line in lines[skip_head:]:
	cols=line.split(",")
	s=float(cols[1])
	x=float(cols[2])
	e=float(cols[3])
	en=float(cols[4])

	ofile.write("%12.5f %12.5f %12.5f %12.5f\n"%(s,x,e,en))

ofile.close()
