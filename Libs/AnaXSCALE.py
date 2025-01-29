import sys,os,math,subprocess
from scipy.interpolate import interp1d
import numpy as np
import matplotlib.pyplot as plt

"""
 SUBSET OF INTENSITY DATA WITH SIGNAL/NOISE >= -3.0 AS FUNCTION OF RESOLUTION
 RESOLUTION     NUMBER OF REFLECTIONS    COMPLETENESS R-FACTOR  R-FACTOR COMPARED I/SIGMA   R-meas  CC(1/2)  Anomal  SigAno   Nano
   LIMIT     OBSERVED  UNIQUE  POSSIBLE     OF DATA   observed  expected                                      Corr

     6.40        3718     992       995       99.7%      20.6%     19.8%     3706    4.35     23.9%    95.6*     1    0.891     351
     4.54        7014    1807      1807      100.0%      23.0%     21.4%     7010    4.43     26.7%    94.3*     5    0.963     753
     3.72        9013    2303      2303      100.0%      22.7%     21.3%     9011    4.58     26.3%    94.2*     1    0.923    1000
     3.22       10322    2734      2734      100.0%      28.2%     25.3%    10319    3.55     32.9%    90.8*     4    0.958    1213
     2.88       10053    3093      3094      100.0%      35.9%     32.8%    10013    2.35     43.1%    81.3*     6    0.993    1362
     2.63       10655    3412      3420       99.8%      52.5%     47.4%    10572    1.42     63.5%    67.2*     1    0.900    1480
     2.44       12766    3743      3748       99.9%      67.5%     63.5%    12733    1.02     80.2%    60.3*     5    0.847    1693
     2.28       14078    4011      4012      100.0%      76.3%     73.1%    14047    0.84     90.0%    57.2*     1    0.802    1826
     2.15       14867    4216      4227       99.7%      91.0%     89.3%    14773    0.61    106.9%    48.3*     2    0.763    1896
    total       92487   26312     26340       99.9%      37.5%     35.1%    92184    2.07     44.2%    90.3*     3    0.877   11574
"""

class AnaXSCALE():
    def __init__(self, xscalelp_path):
        self.xscalelp_path = xscalelp_path
        ifile=open(xscalelp_path,"r")
        self.lines=ifile.readlines()
        ifile.close()

        self.ds2_list=[]
        self.isRead = False

        self.nbin = 10

    def setNbin(self, nbin):
        self.nbin = nbin
        print "NBIN = ",self.nbin

    def getFinalSPG(self):
        for line in self.lines:
            if line.rfind("SPACE_GROUP_NUMBER=")!=-1:
                cols=line.split()
                spgnum=int(cols[1])
        return spgnum

    def getCellParm(self):
        for line in self.lines:
            if line.rfind("UNIT_CELL_CONSTANTS=")!=-1:
                print line
                cols=line.split()
                a=float(cols[1])
                b=float(cols[2])
                c=float(cols[3])
                alph=float(cols[4])
                beta=float(cols[5])
                gamm=float(cols[6])
        return a,b,c,alph,beta,gamm

    def readLog(self,csv_flag=False):
        flag=0
        skip=0
        start=0
        idx=0
        for line in self.lines:
            if line.find("SUBSET OF INTENSITY DATA WITH SIGNAL/NOISE >= -3.0 AS FUNCTION OF RESOLUTION")!=-1:
                start=idx
            idx+=1
        end=idx

        dmin_save=0.0
        cc_half_mon=0.0
        logstr=[]
        self.shell_info=[]
        total_redun=0.0
        shell_counter=0.0
        for i in range(start,end):
            line=self.lines[i]
            if line=="\n":
                continue
            cols=line.split()
            #print cols
            if flag==1 and skip < 3:
                skip+=1
                continue
            if line.find("SUBSET OF INTENSITY DATA WITH SIGNAL/NOISE >= -3.0 AS FUNCTION OF RESOLUTION")!=-1:
                flag=1
                skip+=1
                continue
            if flag==1 and cols[0]=="total":
                break
            if flag==1:
                dmin=float(cols[0])
                ds2=1.0/dmin/dmin
                compl=float(cols[4].replace("%",""))
                rfact=float(cols[5].replace("%",""))
                isigi=float(cols[8])
                n_obs=float(cols[1])
                n_poss=float(cols[2])
                if n_poss != 0.0:
                    redun=n_obs/n_poss
                else:
                    redun=0.0
                cc_half=float(cols[10].replace("%","").replace("*",""))
                self.shell_info.append((ds2,compl,rfact,isigi,n_obs,n_poss,redun,cc_half))

                """
                if cc_half < 50.0:
                    print "%5.1f"%dmin_save
                    break
                """

                dmin_save=dmin
                total_redun+=redun
                shell_counter+=1.0

            if csv_flag==False:
                logstr.append("%9.3f %9.3f %9.3f %9.3f %9.3f %9.3f %9.3f\n"%(dmin,compl,ds2,rfact,isigi,cc_half,redun))
            else:
                logstr.append("%9.3f,%9.3f,%9.3f,%9.3f,%9.3f,%9.3f,%9.3f\n"%(dmin,compl,ds2,rfact,isigi,cc_half,redun))
        logstr.append("# Average redun = %8.4f\n"%(total_redun/shell_counter))
        self.isRead = True
        return logstr

    def getShellInfo(self):
        self.readLog() 
        return self.shell_info

    def determineResolution(self):
        si=self.getShellInfo()
        ds2a=[]
        ccha=[]
        for i in si:
            ds2,compl,rfact,isigi,n_obs,n_poss,redun,cc_half=i
            if compl < 75.0:
                break
            ds2a.append(ds2)
            ccha.append(cc_half)

        xa=np.array(ds2a)
        ya=np.array(ccha)

        xmin=xa.min()
        xmax=xa.max()

        f_line = interp1d(xa, ya)
        f_CS = interp1d(xa, ya, kind='cubic')

        xnew=np.linspace(xmin,xmax,num=100)

        break_flag = False
        for x in xnew:
            y=f_CS(x)
            if y < 50.0:
                print x,math.sqrt(1/x)
                break_flag = True
                break

        if break_flag == False:
            print "resolution limit would be beyond the max resolution in this XSCALE.LP"
        return math.sqrt(1/x)

    def makePlot(self):
        if self.isRead == False:
            self.readLog()
        si=self.shell_info
        ds2a = []
        ccha = []
        isiga = []

        for i in si:
            ds2,compl,rfact,isigi,n_obs,n_poss,redun,cc_half=i
            ds2a.append(ds2)
            ccha.append(cc_half)
            isiga.append(isigi)

        # d*2 .vs. Rmeas
        ds2_na=np.array(ds2a)
        cch_na=np.array(ccha)
        isig_na=np.array(isiga)
    
        #myplot=Plot.Plot()
        #myplot.init()
        outfile="overall.eps"
        plt.legend(loc = 'upper left', fontsilze = 24)
        # The left axis -> CC(1/2)
        fig = plt.figure()
        ax1 = fig.add_subplot(111)
        ln1 = ax1.plot(ds2_na,cch_na,'o-',color='r')

        ax2 = ax1.twinx()
        ln2 = ax2.plot(ds2_na,isig_na,'x-',color='b')

        h1, l1 = ax1.get_legend_handles_labels()
        h2, l2 = ax2.get_legend_handles_labels()
        ax1.legend(h1+h2, l1+l2, loc='lower right')

        ax1.set_xlabel('d*2')
        ax1.set_ylabel('CC(1/2)')

        ax1.grid(True)
        ax2.set_ylabel('<I/sigI>')

        fig.savefig(outfile,dpi=600)

    def checkCChalf(self):
        if self.isRead == False:
            self.readLog()
        si=self.shell_info
        ds2a = []
        ccha = []
        isiga = []
        logisiga = []

        for i in si:
            ds2,compl,rfact,isigi,n_obs,n_poss,redun,cc_half=i
            if isigi > 0.0:
                ds2a.append(ds2)
                ccha.append(cc_half)
                isiga.append(isigi)
                logisiga.append(np.log(isigi))
            else:
                isigi_bad_flag = True

        # For <I/sigI> .vs. CC(1/2) plot
        cch_na=np.array(ccha)
        isig_na=np.array(isiga)
        logisig_na=np.array(logisiga)
        ds2_na=np.array(ds2a)

        outfile="cchalf.eps"
        plt.legend(loc = 'upper left', fontsilze = 24)
        # The left axis -> CC(1/2)
        fig = plt.figure()
        ax1 = fig.add_subplot(111)
        print cch_na,isig_na
        ln1 = ax1.plot(cch_na,isig_na,'o-',color='r')
        ax2 = ax1.twinx()
        ln2 = ax2.plot(cch_na,logisig_na,'x-',color='b')

        h1, l1 = ax1.get_legend_handles_labels()
        h2, l2 = ax2.get_legend_handles_labels()
        ax1.legend(h1+h2, l1+l2, loc='lower right')

        ax1.set_xlabel('CC(1/2)')
        ax1.set_ylabel('<I/sigI>')
        ax1.grid(True)
        ax2.set_ylabel('log(<I/sigI>)')

        fig.savefig(outfile,figsize=(8,6),dpi=600)

    def readDataLines(self):
        lines=open(self.xscalelp_path).readlines()

        line_idx=0
        all_datasets=[]
        shell_flag=False
        read_flag=False

        for line in lines:
            if line.rfind("R-FACTORS FOR INTENSITIES OF DATA SET")!=-1:
                shell_flag=True
                tmpstr=[]
                tmpstr.append(line)
            if shell_flag==True and line.rfind("LIMIT")!=-1:
                #print "PATTERN2"
                read_flag=True
            if read_flag==True:
                if line=="" or line=="\n":
                    continue
                tmpstr.append(line)
            if read_flag==True and (line.rfind("total")!=-1 or line.rfind("***")!=-1):
                #print "PATTERN4"
                read_flag=False
                shell_flag=False
                all_datasets.append(tmpstr)
                #print tmpstr
        return all_datasets

    def makeDataList(self):
        # Read data stat tables
        all_datasets = self.readDataLines()

        n_data=len(all_datasets)

        dlist = []
        for each_data in all_datasets:
            dlist.append(self.analyzeLineForEachData(each_data))

        dlist.sort(key = lambda x:x[1])
        return dlist

    def choose(self, dmin_thresh, overall_r_thresh, nbatch = 5):
        dlist = self.makeDataList()

        # resolution limit list
        dmin_list=[]
        overall_rmin = 9999.9999
        overall_rmax = -9999.9999
        for dname, dmin, lowr, ovr in dlist:
            exist_flag = False
            if len(dmin_list) == 0:
                dmin_list.append(dmin)
            else:
                for dexist in dmin_list:
                    if dexist == dmin:
                        exist_flag = True
                        continue
                if exist_flag == False:
                    dmin_list.append(dmin)
            if ovr < overall_rmin:
                overall_rmin = ovr
            elif ovr >= overall_rmax:
                overall_rmax = ovr

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
            else:
                n_reject += 1
            ofile2.write("%8.2f %8.2f %8.2f %100s\n"%(dmin,lowr,ovr,dname))

        print "N(good),N(reject) = ",n_good,n_reject
        return n_good,n_reject

    def analyzeLineForEachData(self, lines_eachdata):
        # mainly checks R-symm values
        # bad_flag: if Rsym in shell shows 'negative' value,
        # the flag becomes True
        # dmin_this_data: dmin value in 'positive' Rvalue
        bad_flag = False
        if self.nbin == 10:
            search_length = 11
        elif self.nbin == 20:
            search_length = 22
        #print "HEAD = ",lines_eachdata[2]
        #print "TAIL = ",lines_eachdata[search_length]
        for line in lines_eachdata[2:search_length]:
            rsym = float((line.replace("%"," ")).split()[1])
            print "line = ANA:",line,rsym
            if rsym < 0.0:
                bad_flag = True
                dmin_this_data = dsave
            else:
                print line.replace("%"," ").split()
                dsave = float((line.replace("%"," ")).split()[0])
        # The lowest shell Rsymm
        lowest_res_rsym=float((lines_eachdata[2].replace("%"," ")).split()[1])
        # Overall Rsymm
        total_rsym=float((lines_eachdata[search_length].replace("%"," ")).split()[1])
        # Data name
        dname = "INPUT_FILE=%s"% lines_eachdata[0].split()[6]
        # dmin for this data (maximum resolution)
        if bad_flag == False:
           dmin_this_data = float((lines_eachdata[search_length-1].replace("%"," ")).split()[0])

        # Storing data
        rtn_data = dname, dmin_this_data, lowest_res_rsym, total_rsym
        return rtn_data

if __name__=="__main__":
    ac=AnaXSCALE(sys.argv[1])

    cells = ac.getCellParm()
    print cells
    #resol = ac.get_resolution()
    spg = ac.getFinalSPG()
    print spg
