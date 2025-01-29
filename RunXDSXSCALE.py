import os,sys,math

class RunXDSXSCALE():
    def __init__(self, proc_dir):
        abs_path = os.path.abspath(proc_dir)
        self.proc_dir = abs_path
        print "init"

    def writeHeader(self):
        lines=[]
        lines.append("#!/bin/csh\n")
        lines.append("#$ -cwd\n")
        lines.append("#$ -o %s\n"%self.proc_dir)
        lines.append("#$ -e %s\n"%self.proc_dir)
        self.isHead=True
        return lines

    def writeOnly(self, comfile, comlines):
        ofile = open(comfile,"w")
        for l in comlines:
            ofile.write("%s"%l)
        ofile.close()

    def runXSCALE(self,option = "simple"):
        if option == "simple":
            self.runSimple()
        #elif option == "clean":
            #self.runClean()
        elif option == "convenient":
            self.runConvenient()

    def runSimple(self):
        comlines = []
        comfile = "%s/run.com"%self.proc_dir
        comlines += self.writeHeader()
        comlines += "cd %s\n"%self.proc_dir
        comlines += "xscale_par\n"
        self.writeOnly(comfile, comlines)

        os.system("chmod 744 %s"%comfile)
        os.system("qsub %s"%comfile)

    def runConvenient(self):
        comlines = []
        comfile = "%s/run.com"%self.proc_dir
        comlines += self.writeHeader()
        comlines += "cd %s\n"%self.proc_dir
        comlines += "xscale_par\n"
        comlines += "rm -f *.cbf\n"
        comlines += "xds2mtz.py xscale.hkl\n"
        comlines += "phenix.merging_statistics ./xscale.hkl > merge.dat"
        self.writeOnly(comfile, comlines)

        os.system("chmod 744 %s"%comfile)
        os.system("qsub %s"%comfile)

if __name__=="__main__":
    rxs = RunXDSXSCALE("./")
    rxs.runXSCALE()
