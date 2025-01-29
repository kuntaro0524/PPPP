import os,sys,math,numpy

sys.path.append("/isilon/BL32XU/BLsoft/PPPP/")

import DirectoryProc

dp = DirectoryProc.DirectoryProc(sys.argv[1])

dires = dp.findDirs()

print dires
