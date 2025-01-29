import sys,os,math

lines = open(sys.argv[1],"r").readlines()

for line in lines:
    if line.rfind("file a b") != -1:
        continue
    else:
        print line.split()[0]
