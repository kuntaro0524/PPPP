import os,sys,math
import ChooseAndMakeXSCALEINP
import DirectoryProc
import RunXDSXSCALE

if __name__=="__main__":

    if len(sys.argv) != 3:
        print "# sys.argv[1]: XSCALE.LP"
        print "# sys.argv[2]: XSCALE.INP Header information"
        sys.exit()

    resol_list = [2.8, 3.0, 3.1, 3.2, 3.3, 3.4, 3.5]
    rfact_list = [500.0, 400.0, 300.0, 200.0, 150.0, 100.0]

    dp = DirectoryProc.DirectoryProc("./")
    camx = ChooseAndMakeXSCALEINP.ChooseAndMakeXSCALEINP(sys.argv[1],sys.argv[2])
    camx.prep()

    for dthresh in resol_list:
        for rthresh in rfact_list:
            camx.reset_list()
            # select datasets with higher resolution than 'dthresh'
            nresol = camx.choose_resol(dthresh)
            # select datasets with lower overall Rsymm than 'rthresh'
            noverr = camx.choose_overall_r(rthresh)
        
            dirname = "./%3.1fA_%5.1f"%(dthresh,rthresh)
            abs_path = dp.roundMakeDir(dirname)
            "from roundMakeDir = ",abs_path
            # make XSCALE.INP for each scaling
            camx.makeXSCALEINP(abs_path,add_path="../")
        
            ofile = open("%s/choose.log"%abs_path,"w")
            ofile.write("Resolution cutoff %8.2f A\n"%dthresh)
            ofile.write("Overall R  cutoff %8.1f percent\n"%rthresh)
            ofile.write("N(resol)=%5d N(overall_R)=%5d\n"%(nresol,noverr))

            # qsub file
            #camx.makeXSCALEINP(abs_path,add_path="../")
            rxs = RunXDSXSCALE.RunXDSXSCALE(abs_path)
            # conducting everything for scaling
            rxs.runXSCALE(option = "convenient")
            print abs_path
