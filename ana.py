from AnalyzePeak import *

if __name__=="__main__":
                ana=AnalyzePeak(sys.argv[1])

		# PREFIX
		fname=sys.argv[1]
		outfig=fname.replace(".scn",".png")
		
		comment=fname
        	fwhm,center=ana.analyzeAll2("Zrel[um]","Intensity",outfig,4,6,comment,"OBS","FCEN")
		print "%12.4f %12.4f"%(fwhm,center)
