import os,sys,math

lines = open(sys.argv[1],"r").readlines()
resol_thresh = float(sys.argv[2])


ofile = open("data_highres.csv", "w")
ofile.write("topdir,name,anomalous\n")

n_good = 0
n_read = 0
for line in lines:
    n_read += 1
    cols = line.split()
    filepath = cols[0]
    resol = float(cols[1])
    if resol < resol_thresh:
        n_good += 1
        ofile.write("%s,good,no\n" % filepath[:filepath.rfind("/")])

print "Read/Good = ", n_read, n_good
