import os,sys,math

copy_file=sys.argv[1]
listlines=open(sys.argv[2],"r").readlines()

for line in listlines:
	com="cp %s %s"%(copy_file,line)
	os.system(com)
