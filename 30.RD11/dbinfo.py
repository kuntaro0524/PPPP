import os,sys,numpy

sys.path.append("/isilon/BL45XU/BLsoft/PPPP/10.Zoo/Libs/")

import DBinfo
import ESA

if __name__ == "__main__":
    esa = ESA.ESA(sys.argv[1])
    esa.prepReadDB()
    esa.getTableName()
    esa.listDB()
    conds = esa.getDict()

    for each_db in conds:
        isDone = each_db['isDone']

        if isDone == 0:
            continue

        dbinfo = DBinfo.DBinfo(each_db)
        pinstr = dbinfo.getPinStr()
        good_flag = dbinfo.getGoodOrNot()

        constime = dbinfo.getMeasTime()

        print dbinfo.puck, dbinfo.pin, dbinfo.dose_ds, dbinfo.ntimes, dbinfo.reduced_fact
