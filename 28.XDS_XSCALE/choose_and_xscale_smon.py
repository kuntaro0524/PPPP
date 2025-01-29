import os,sys,math, numpy
sys.path.append("/isilon/BL32XU/BLsoft/PPPP/")
sys.path.append("/isilon/BL32XU/BLsoft/PPPP/28.XDS_XSCALE")
import ChooseAndMakeXSCALEINP
import RunXDSXSCALE
import DirectoryProc

if __name__=="__main__":

    if len(sys.argv) != 7:
        print "# sys.argv[1]: XSCALE.LP"
        print "# sys.argv[2]: XSCALE.INP Header information"
        print "# sys.argv[3]: NBATCH information -> For large wedge merging, set 'minus' value; ex) -1 to skip setting"
        print "# sys.argv[4]: high resolution limit"
        print "# sys.argv[5]: low resolution limit"
        print "# sys.argv[6]: number of resolution cuts"
        sys.exit()

    rfact_list = [25,50,75,100]

    dp = DirectoryProc.DirectoryProc("./")
    #    def __init__(self, xscalelp, input_header, nbin = 20):
    xscalelp = sys.argv[1]
    head_xscale = sys.argv[2]
    nbatch = int(sys.argv[3])
    high_res = float(sys.argv[4])
    low_res = float(sys.argv[5])
    n_trials = int(sys.argv[6])

    resol_list = numpy.linspace(high_res, low_res, n_trials)

    camx = ChooseAndMakeXSCALEINP.ChooseAndMakeXSCALEINP(xscalelp, head_xscale)
    camx.prep()

    for dthresh in resol_list:
        for rthresh in rfact_list:
            camx.reset_list()
            # select datasets with higher resolution than 'dthresh'
            nresol = camx.choose_resol(dthresh)
            # select datasets with lower overall Rsymm than 'rthresh'
            noverr = camx.choose_overall_r(rthresh)
        
            dirname = "./%3.1fA_rfac_%d"%(dthresh,rthresh)
            # making directories
            if os.path.exists(dirname)==False:
                abs_path = os.path.abspath(dirname)
                os.makedirs(abs_path)

            "from roundMakeDir = ",abs_path
            # make XSCALE.INP for each scaling
            camx.makeXSCALEINP(abs_path,add_path="../",nbatch=nbatch)
        
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
