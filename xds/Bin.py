import numpy, math, sys
import matplotlib.pyplot as plt

class Bin():

    def __init__(self, start, end, nbin, mode="linear"):
        self.start = start
        self.end = end
        self.nbin = nbin
        self.mode = mode
        self.isInit = False

    def init(self):
        if self.isInit == True:
            return
        self.bins = numpy.linspace(self.start, self.end, self.nbin)
        print "LEN=", len(self.bins), self.bins
        self.isInit = True

    def putValues(self, values):
        print type(values)
        self.init()
        self.bin_indice = numpy.digitize(values, self.bins)
        return self.bin_indice

    def makeBinArray(self, values):
        self.putValues(values)


if __name__=="__main__":
    import XDS_ASCII
    xdsas=XDS_ASCII.XDS_ASCII(sys.argv[1])
    #print "%s %10.1f"%(sys.argv[1],xdsas.calcDP())
    xdsas.readMinimumInfo()

    print "LOGLOG=", len(xdsas.zd)
    zenhan_dp = 0.0
    kouhan_dp = 0.0
    for zd, iobs in zip(xdsas.zd, xdsas.iobs):
        if zd < 51.0:
            zenhan_dp += iobs
        else:
            kouhan_dp += iobs

    print "%8.2f, %8.2f" % (zenhan_dp, kouhan_dp)

    bin = Bin(0,100,11)
    bin_indice = bin.putValues(xdsas.zd)
    print "len=", len(bin_indice)
    sum = numpy.zeros(10)

    for index, iobs, zd in zip(bin_indice, xdsas.iobs, xdsas.zd):
        #print zd, index, iobs
        sum[index-1] += iobs

    for index in range(0, len(sum)):
        print "HIST: %5d %12.3f" % (index, sum[index])