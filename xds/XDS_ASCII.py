import sys,os,numpy

class XDS_ASCII():
    def __init__(self, xds_ascii_hkl):
        self.xds_ascii_file = xds_ascii_hkl
        self.iobs_list = []
        self.isRead = False

        self.h = []
        self.k = []
        self.l = []
        self.iobs = []
        self.sigma = []
        self.xd = []
        self.yd = []
        self.zd = []
        self.peak = []
        self.isigi = []

    def readLines(self):
        if self.isRead == True:
            return
        self.lines=open(self.xds_ascii_file).readlines()
        self.isRead = True

    def readMinimumInfo(self):
        self.readLines()

        for line in self.lines:
            cols = line.split()
            if line.rfind("UNIT_CELL_CONSTANTS=") != -1:
                self.a = float(cols[1])
                self.b = float(cols[2])
                self.c = float(cols[3])
                self.alph = float(cols[4])
                self.beta = float(cols[5])
                self.gamm = float(cols[6])
            if line.rfind("WAVELENGTH") != -1:
                self.wavelength = float(cols[1])
            if len(cols) > 10:
                self.h.append(int(cols[0]))
                self.k.append(int(cols[1]))
                self.l.append(int(cols[2]))
                self.sigma.append(float(cols[4]))
                self.xd.append(float(cols[5]))
                self.yd.append(float(cols[6]))
                self.zd.append(float(cols[7]))
                peak = float(cols[9]) / 100.0
                self.peak.append(peak)
                iobs = float(float(cols[4]))
                iobs_corr = iobs * peak
                #self.isigi.append(isigi)
                self.iobs.append(iobs_corr)

    def calcDP(self):
        self.readLines()

        total_i=0.0
        for line in self.lines:
            # skip comment lines
            if line[0]=="!":
                continue
            cols=line.split()
            iobs=float(cols[3])
            self.iobs_list.append(iobs)
            total_i+=iobs
        #self.isRead=True
        return total_i


"""
0123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890
          1         2         3         4         5         6         7         8         9
    -2    -2     0  6.952E+02  4.673E+01  1236.1  1252.2     47.7   0.03596 100  61   39.67
"""
if __name__=="__main__":
    xdsas=XDS_ASCII(sys.argv[1])
    #print "%s %10.1f"%(sys.argv[1],xdsas.calcDP())
    xdsas.readMinimumInfo()

    #print "LOGLOG=", len(xdsas.zd)
    zenhan_dp = 0.0
    kouhan_dp = 0.0
    for zd, iobs in zip(xdsas.zd, xdsas.iobs):
        if zd < 51.0:
            zenhan_dp += iobs
        else:
            kouhan_dp += iobs

    print "%8.2f, %8.2f" % (zenhan_dp, kouhan_dp)
