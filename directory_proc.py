import os,sys,math,glob
import time
import DirectoryProc
import AnaCORRECT
import XDSascii
import Fitting
import AnaDSlog

if __name__ == "__main__":
	#p=DirectoryProc.DirectoryProc(sys.argv[1])
	#bsslog_searchname=sys.argv[2]
        dp=DirectoryProc.DirectoryProc(sys.argv[1])
    	phosec=float(sys.argv[2])

        dlist=dp.getDirList()

        # _kamoproc directory
        for d in dlist:
                cols=d.split('/')
                dataname=cols[-1]
                # XDS_ASCII.HKL searching
                search_path="%s/../_kamoproc/%s/"%(d,dataname)
                xds_ascii_list= dp.findTargetFileIn(search_path,"XDS_ASCII_fullres.HKL")
                correctlp_list= dp.findTargetFileIn(search_path,"CORRECT_fullres.LP")
                # XDS_ASCII.HKL searching
                search_path="%s/data/"%(d)
                #print search_path
                bsslogpath= dp.findTargetFileIn(search_path,"cry00_000.log")

		# SORT
                xds_ascii_list.sort()
                correctlp_list.sort()

		print dataname

		# Analysing CORRECT.LP
		ofile=open("correct_%s.dat"%dataname,"w")
		for tfile in correctlp_list:
			ac=AnaCORRECT.AnaCORRECT(tfile)
			logstr=ac.read()
	
			ofile.write("## %s ##\n"%tfile)
			for log in logstr:
				ofile.write("%s"%log)
			ofile.write("\n\n")
		ofile.close()

		# Intensity from XDS_ASCII.HKL
		ofile=open("intensity_%s.dat"%dataname,"w")
		file_index=1
		for each_ascii in xds_ascii_list:
			print each_ascii
        		xdsas=XDSascii.XDSascii(each_ascii)
        		ofile.write("%30s %5d %10.1f\n"%(each_ascii,file_index,xdsas.calcDP()))
			file_index+=1
		ofile.close()

		# Analyse
    		ft=Fitting.Fitting()
    		expected_half_ds=ft.fittingOnFile("intensity.dat",1,2)
	
    		an=AnaDSlog.AnaDSlog(bsslogpath)
    		logstr,limit_density=an.prep(phosec,expected_half_ds)
	
		ofile=open("analyze.log","w")
		for line in logstr:
			ofile.write("%s"%line)
    		comment="Limit density = %5.1e photons/um^2"%limit_density
    		ft.makePlotPNG("analyzed.png",comment=comment)
	
    		print "%s %8.3e"%(sys.argv[1],limit_density)
