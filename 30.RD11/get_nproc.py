import os,sys,math

infile = "/proc/cpuinfo"

lines = open(infile, "r").readlines()

for line in lines:
    if line.rfind("processo") != -1:
        nproc = int(line.split()[2])

nproc += 1
print nproc