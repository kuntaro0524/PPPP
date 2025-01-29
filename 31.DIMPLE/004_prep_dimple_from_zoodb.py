import os, sys, math, logging
sys.path.append("/isilon/BL32XU/BLsoft/PPPP/10.Zoo/Libs")
sys.path.append("/isilon/BL32XU/BLsoft/PPPP/Libs")
import DBinfo
import ESA
import DirectoryProc

beamline = "BL32XU"

if __name__ == "__main__":
    esa = ESA.ESA(sys.argv[1])
    esa.prepReadDB()
    conds = esa.getDict()

    csv_filename = "dimple_prep.csv"
    csvfile = open(csv_filename,"w")

    csvfile.write("puck_pinid,sample_name,xds_hkl_file\n")

    # Logging setting
    logname = "./prep_dimple.log"
    logging.config.fileConfig('/isilon/%s/BLsoft/PPPP/10.Zoo/Libs/logging.conf' % beamline, defaults={'logfile_name': logname})
    logger = logging.getLogger('DIMPLE')

    n_good = 0
    n_ng = 0
    n_process_succeeded = 0
    # All pin information will be analyzed from zoo.db information
    # p -> each pin information
    for p in conds:
        dbinfo = DBinfo.DBinfo(p)
        # 'isDS' is evaluated. -> normal termination : return 1
        n_good += dbinfo.getStatus()

        # is data collection completed?
        good_flag = dbinfo.getGoodOrNot()
        log_comment = dbinfo.getLogComment()
        mode = dbinfo.mode

        if good_flag == True:
            puckid,pinid = dbinfo.getPinInfo()
            sample_name = dbinfo.sample_name
            if dbinfo.mode == "multi":
                continue

            pin_dir = dbinfo.getPinStr()
            root_dir = dbinfo.root_dir
            kamopath = os.path.join(root_dir, "_kamoproc")
            procpath = os.path.join(kamopath, pin_dir)
            dipro = DirectoryProc.DirectoryProc(procpath)
            flist,plist = dipro.findTarget("XDS_ASCII.HKL")
            if len(flist) == 0:
                logger.info("No XDS_ASCII.HKL: Data processing failed for %s" % pin_dir)
            else:
                xds_hkl_file = flist[0]
                n_process_succeeded += 1

            # Output to CSV file
            csvfile.write("%s,%s,%s\n" % (pin_dir,sample_name,xds_hkl_file))

        # Not good pins
        else:
            continue

    logger.info("NDS processed = %5d" % n_good)
    logger.info("%5d data list is written into %s" % (n_process_succeeded, csv_filename))
