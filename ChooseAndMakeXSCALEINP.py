import os,sys,math,copy
import AnaXSCALE

class ChooseAndMakeXSCALEINP():
    def __init__(self, xscalelp, input_header, nbin = 20):
        self.input_header = input_header
        self.ac=AnaXSCALE.AnaXSCALE(xscalelp)
        self.isPrep = False
        self.nbin = nbin

    def prep(self):
        # the number of shells
        self.ac.setNbin(20)
        self.datalist = self.ac.makeDataList()
        self.datalist_orig = copy.deepcopy(self.datalist)
        #for dname, dmin, lowr, ovr in self.datalist:
            #print "BEFORE = %8.2f %8.2f %s"%(dmin, ovr, dname)
        self.isPrep = True

    def reset_list(self):
        self.datalist = copy.deepcopy(self.datalist_orig)

    def choose_resol(self, dmin_thresh):
        if self.isPrep == False:
            self.prep()
        # resolution limit list
        new_list = []
        for dname, dmin, lowr, ovr in self.datalist:
            if dmin <= dmin_thresh:
                new_list.append((dname,dmin,lowr,ovr))

        self.datalist = new_list
        #for dname, dmin, lowr, ovr in self.datalist:
            #print "AFTER = %8.2f %8.2f %s"%(dmin, ovr, dname)

        return len(self.datalist)

    def choose_overall_r(self, r_thresh):
        if self.isPrep == False:
            self.prep()
        # resolution limit list
        new_list = []
        for dname, dmin, lowr, ovr in self.datalist:
            if ovr <= r_thresh:
                new_list.append((dname,dmin,lowr,ovr))

        self.datalist = new_list
        #for dname, dmin, lowr, ovr in self.datalist:
            #print "FINAL = %8.2f %8.2f %s"%(dmin, ovr, dname)
        return len(self.datalist)

    def makeXSCALEINP(self,abs_path,add_path,nbatch = 5):
        print "ChooseAndMakeXSCALEINP.makeXSCALEINP = ABS", abs_path
        print "ChooseAndMakeXSCALEINP.makeXSCALEINP = ADD", add_path
        # header lines
        header_lines = open(self.input_header,"r").readlines()
        # XSCALE.INP making
        ofile = open("%s/XSCALE.INP"%abs_path,"w")
        n_good = 0
        n_reject = 0
        for li in header_lines:
            ofile.write("%s"%li)

        for dname, dmin, lowr, ovr in self.datalist:
            # File path from the previous run
            new_path = dname.replace("INPUT_FILE=../","INPUT_FILE=%s/../"%add_path)
            ofile.write("%s\n"% new_path)
            ofile.write("NBATCH= %d\n"%nbatch)
            n_good += 1

        ofile.close()

    def analyzeBigData(self):
        # Overall R-factors bin
        print "OVER=",overall_rmax,overall_rmin
        tot_width = overall_rmax - overall_rmin
        bin_width = tot_width/10.0

        print dmin_list,len(dmin_list)
        # Frequency counter
        freq_dmin = [0]*len(dmin_list)
    
        # Making histogram of overall Rfactor
        for dname, dmin, lowr, ovr in dlist:
            index_ = dmin_list.index(dmin)
            freq_dmin[index_] += 1
    
        for dmin,freq in zip(dmin_list,freq_dmin):
            print "%8.2f %5d"%(dmin,freq)
    
        # XSCALE.INP making
        ofile = open("INPUT.DAT","w")
        ofile2 = open("datalist.dat","w")
        n_good = 0
        n_reject = 0
        for dname, dmin, lowr, ovr in dlist:
            if dmin <= dmin_thresh and ovr <= overall_r_thresh:
                ofile.write("%s\n"% dname)
                ofile.write("NBATCH= %d\n"%nbatch)
                n_good += 1
    
if __name__=="__main__":
    camx = ChooseAndMakeXSCALEINP(sys.argv[1],sys.argv[2])
    res_thresh = float(sys.argv[3])
    r_thresh = float(sys.argv[4])
    nresol = camx.choose_resol(res_thresh)
    noverr = camx.choose_overall_r(r_thresh)

    dirname = "./%3.1fA_%5.1f"%(res_thresh,r_thresh)
    os.mkdir(dirname)
    abs_path = os.path.abspath(dirname)

    ofile = open("%s/choose.log"%abs_path,"w")
    ofile.write("Resolution cutoff %8.2f A\n"%float(sys.argv[3]))
    ofile.write("Overall R  cutoff %8.1f percent\n"%float(sys.argv[4]))
    ofile.write("N(resol)=%5d N(overall_R)=%5d"%(nresol,noverr))

    camx.makeXSCALEINP(abs_path,add_path="../")
