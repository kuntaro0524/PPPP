import os,sys

class LibSPG():

    def __init__(self, clibd_path="/Applications/ccp4-7.0/lib/data/symop.lib"):
        if os.environ['CLIBD'] != "":
            clibd_path = os.environ['CLIBD']
        self.clibd = os.path.join(clibd_path ,"symop.lib")
        self.lines = open(self.clibd,"r").readlines()

    def get_spg_str(self, line):
        cols = line.split()
        spg = cols[3]
        return spg

    def search_spgnum(self, spgnum):
        for line in self.lines:
            cols = line.split()
            if len(cols) > 5:
                #print len(cols),":",line
                t_spgnum = int(cols[0])
                #print "SPGNUM=", int(cols[0])
                if spgnum == t_spgnum:
                    return(self.get_spg_str(line))


if __name__=="__main__":
    lll = libSPG()
    print lll.search_spgnum(92)
