import os,sys,math

target_string=sys.argv[2]
replace_string=sys.argv[3]

ofile=open("formerge_new.lst","w")
for line in open(sys.argv[1],"r").readlines():
    ofile.write("%s"% line.replace(target_string,replace_string))

ofile.close()

