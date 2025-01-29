import os, sys

lines = open(sys.argv[1], "r").readlines()

for line in lines:
    if line.rfind("class") !=-1:
        print line
    if line.rfind("def") != -1:
        print line,
