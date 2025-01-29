import os, sys, math, glob
import time

sys.path.append("/isilon/BL32XU/BLsoft/PPPP/")

import DirectoryProc
sys.path.append("/isilon/BL32XU/BLsoft/PPPP/15.MergedCBF/")
import MergeCBF

class DataBunch:
    def __init__(self):
        self.data_list = []
        self.max_dnum = -99999
        self.max_crynum = -99999

    def checkExists(self, crynum, dnum):
        for cn, dn in self.data_list:
            if cn == crynum and dn == dnum:
                return True
        return False

    def append(self, crynum, dnum):
        if self.checkExists(crynum, dnum) == False:
            if self.max_dnum < dnum:
                self.max_dnum = dnum
            if self.max_crynum < crynum:
                self.max_crynum = crynum

            self.data_list.append((crynum, dnum))

    def getList(self):
        return self.data_list


if __name__ == "__main__":
    #dp = DirectoryProc.DirectoryProc(sys.argv[1])
    cbf_path = sys.argv[1]
    logfiles = glob.glob("%s/*.log" % cbf_path)
    db = DataBunch()

    # For all log files
    for logfile in logfiles:
        filename_cols = logfile.split("/")[-1].split("_")
        prefix = filename_cols[0]
        # Analyzing file names
        for compo in filename_cols:
            if compo.rfind("cry") != -1:
                if compo.rfind("log") != -1:
                    continue
                else:
                    #print prefix, compo, logfile
                    crynum = int(compo.replace(".log","").replace("cry",""))
                    dnum = int(logfile.split(prefix)[-1].split("_")[-2])

                    db.append(crynum, dnum)

    all_list = db.getList()
    all_list.sort()

    n_sum_time = db.max_dnum
    #n_sum_time = 1

    nsum_rotation = 10
    nimg_per_data = 100
    for cryindex in range(1, db.max_crynum + 1):
        cbf_prefix = "%s/%s_cry%02d" % (cbf_path, prefix, cryindex)

        for sum_index in range(1, n_sum_time+1):
            dose = sum_index * 5
            outprefix = "cry%02d_%02dMGy" % (cryindex, dose)
            #print cbf_prefix, outprefix

            mcbf = MergeCBF.MergeCBF()
            mcbf.setNproc(100)
            print "###############", cbf_prefix, sum_index, nsum_rotation, nimg_per_data, outprefix
            mcbf.sumDoseSlicingPhiSlicing(cbf_prefix, sum_index, nsum_rotation, nimg_per_data, outprefix, dphi=0.1)

