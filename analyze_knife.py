import os
import sys
import  pylab
from AnalyzePeak import *
from File import *
from scipy.interpolate import splrep,splev

if __name__=="__main__":

		if len(sys.argv)!=2:
			print "Usage: PROGRAM SCANFILE"
			sys.exit(1)

		filename=sys.argv[1]
		prefix=filename.replace(".scn","")
		ana=AnalyzePeak(sys.argv[1])
		
                drvfile="%s_drv.scn"%prefix
                outfig="%s_drv.png"

                #fwhm,center=ana.anaK("X","Y","TEST")
                fwhm,center=ana.anaK("X","Y","TEST")
        	#fwhm,center=ana.analyzeKnife("X","Y",drvfile,outfig,"TEST",opt="FWHM")

		print "ANANNNANNANNA"
                print fwhm,center
		print "ANANNNANNANNA"
