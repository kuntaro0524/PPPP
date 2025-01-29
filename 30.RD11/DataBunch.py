import os, sys, math, glob
import time

sys.path.append("/isilon/BL32XU/BLsoft/PPPP/")

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