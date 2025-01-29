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

    """
    if len(sys.argv) != 4:
        print "PROG CBF_PATH DOSE_PER_SET[MGy] NPROC"
        sys.exit()
    """

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
        good_flag = dbinfo.getGoodOrNot()

        puckdir = "%s-%02d" % (dbinfo.puck, dbinfo.pin)
        #print puckdir, dbinfo.isDS, dbinfo.n_mount
        data_dir = "%s/data%02d/" % (puckdir, dbinfo.n_mount)
        data_absd = os.path.abspath(data_dir)

        if os.path.exists(data_dir) == True:
            cbf_list = glob.glob("%s/*00001.cbf" % data_dir)
            if len(cbf_list) != 0:
                print "%s CBF exists!" % data_dir
            else:
                print "Skipping"
                continue
            # Checking already processed
            proc_dir = "%s/DoseSum/" % data_absd

            # Process is skipped when 'DoseSum' directory exists already.
            if os.path.exists(proc_dir):
                cbf_list = glob.glob("%s/*00001.cbf" % proc_dir)
                if len(cbf_list) != 0:
                    print "Already processed"
                    continue
            else:
                os.makedirs(proc_dir)
        else:
            print "Skipping"
            continue

        # Main processing loop
        #print dbinfo.puck, dbinfo.pin, dbinfo.dose_ds, dbinfo.ntimes, dbinfo.reduced_fact
        dose_per_data = dbinfo.dose_ds * dbinfo.reduced_fact

        if dbinfo.reduced_fact == 1.0:
            print "No need to proceed 'dose slicing'"
            continue
        # COMFILE
        comname = "%s.com" % puckdir
        comfile = open(comname, "w")
        comfile.write("#!/bin/csh\n")
        comfile.write("#$ -cwd\n")
        comfile.write("#$ -o %s\n" % proc_dir)
        comfile.write("#$ -e %s\n" % proc_dir)

        comfile.write("cd %s/\n" % proc_dir)
        command_line = "set NPROC=`yamtbx.python ~/PPPP/30.RD11/get_nproc.py`\n"
        comfile.write("%s" % command_line)
        command_line = "yamtbx.python ~/PPPP/30.RD11/sumup_cbf_rotation_doseslice.py %s %s $NPROC\n" % (data_absd, dose_per_data)
        comfile.write("%s" % command_line)

        os.system("chmod a+x %s" % comname)
