import os, sys, math, glob
import time

sys.path.append("/isilon/BL45XU/BLsoft/PPPP/")
sys.path.append("/isilon/BL45XU/BLsoft/PPPP/10.Zoo/Libs")

import DirectoryProc
sys.path.append("/isilon/BL45XU/BLsoft/PPPP/15.MergedCBF/")
import MergeCBF
import DBinfo
import ESA
import DataBunch

if __name__ == "__main__":

    dbfile = sys.argv[1]

    esa = ESA.ESA(dbfile)
    esa.prepReadDB()
    esa.getTableName()
    esa.listDB()
    conds = esa.getDict()

    ana_data_list = []
    for each_db in conds:
        isDone = each_db['isDone']

        dbinfo = DBinfo.DBinfo(each_db)
        pinstr = dbinfo.getPinStr()

        puckdir = "%s-%02d" % (dbinfo.puck, dbinfo.pin)

        data_dir = "%s/data%02d/" % (puckdir, dbinfo.n_mount)
        data_absd = os.path.abspath(data_dir)

        if os.path.exists(data_dir) == True:
            proc_dir = "%s/TEST/" % data_absd

            if os.path.exists(proc_dir):
                cbf_list = glob.glob("%s/*00001.cbf" % proc_dir)
                if len(cbf_list) != 0:
                    print "This directory should be changed to DoseSum/"
                    command = "mv %s %s/DoseSum/" % (proc_dir, data_absd, )
                    print command
            else:
                proc_dir = "%s/DoseSum/" % data_absd
                if os.path.exists(proc_dir):
                    print "%s DoseSum exits!" % proc_dir