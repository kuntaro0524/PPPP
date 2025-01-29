import os,sys

lines=open(sys.argv[1],"r").readlines()

for line in lines:
	command="\\rm %s"%line.strip()
	print command
	os.system(command)
