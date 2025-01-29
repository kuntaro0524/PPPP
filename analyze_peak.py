from AnalyzePeak import *
import sys

ana=AnalyzePeak(sys.argv[1])

pngfilename=sys.argv[1].replace(".scn",".png")
comment=""
fwhm,center=ana.analyzeAll("stageZ[mm]","Intensity",pngfilename,comment,"OBS","FCEN")

print fwhm,center
