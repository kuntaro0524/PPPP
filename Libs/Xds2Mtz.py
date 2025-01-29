import os,sys,math,numpy,scipy,subprocess

"""
  -h, --help            show this help message and exit
  -d DIR, --dir=DIR     output directory
  -x, --xtriage         run phenix.xtriage
  -t, --truncate        use ctruncate to estimate F
  -m, --multiplicity    Add multiplicity info
  -a, --anomalous       force anomalous
  --dmin=DMIN           high resolution cutoff
  --dmax=DMAX           low resolution cutoff
  -r FLAG_SOURCE, --copy-test-flag=FLAG_SOURCE
  --add-test-flag       
  --space-group=SG      Space group number or name
"""
    
class Xds2Mtz: 
    def __init__(self, xds_ascii_path):
        self.xds_ascii_path = xds_ascii_path
        self.options = ""
        self.output_path = os.path.join(xds_ascii_path, "ccp4")

    def addFreeRflag(self):
        self.options += " --add-test-flag"

    def setOutputPath(self, output_path):
        self.output_path = output_path
        self.options += " -d %s" % self.output_path

    def isAnomalous(self):
        self.options += " -a"

    def setSPG(self, symm):
        self.options += " --space-group=%s" % symm

    def setReferenceFlagFile(self, ref_mtz):
        self.options += " -r %s" % ref_mtz

    # run xds2mttz.py on KAKI cluster
    def runXDS2MTZ(self,output_path="ccp4/"):
        self.setOutputPath(output_path)
    
        #XDS2MTZ command line
        command = "xds2mtz.py %s %s" % (self.options, self.xds_ascii_path)
        print command
        logs = subprocess.Popen(
            command, stdout=subprocess.PIPE,
            shell=True).communicate()[0]

        lines = logs.split('\n')

        for line in lines:
            print "logline in runXDS2MTZ",line

        return True

if __name__ == "__main__":

    xds2mtz = Xds2Mtz(sys.argv[1])
    xds2mtz.setSPG("P43212")
    # output directory can be defined
    #xds2mtz.runXDS2MTZ("/isilon/BL32XU/TMP/")
    # output is set to the current directory
    xds2mtz.runXDS2MTZ()
