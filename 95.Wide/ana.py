from AnalyzePeak import *

if __name__=="__main__":
                ana=AnalyzePeak(sys.argv[1])
		outfig="colli.png"
		comment="test"
        	fwhm,center=ana.analyzeAll("dtheta1[pulse]","Intensity",outfig,comment,"OBS","FCEN")
		print fwhm,center
