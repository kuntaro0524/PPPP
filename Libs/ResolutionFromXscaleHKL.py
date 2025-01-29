import os,sys,math,subprocess
import MyException
sys.path.append("/isilon/BL32XU/BLsoft/PPPP/")

class ResolutionFromXscaleHKL:
    def __init__(self, xscalehkl_path):
        self.xscalehkl_path = xscalehkl_path
        self.proc_path = xscalehkl_path[:xscalehkl_path.rfind("/")]
        self.resol_info = ".resol_dat"
        self.isGot = False
        self.resol = -9999.9999

    def checkReady(self):
        # Check if the resolution calculation has been done or not
        resol_info_path = os.path.join(self.proc_path, self.resol_info)

        if os.path.exists(resol_info_path) == True:
            lines = open(resol_info_path,"r").readlines()
            res_str = lines[0]
            if res_str.rfind("FAILED") != -1:
                raise MyException.GetResolutionFailed("ResolutionFromXscaleHKL: Resolution calculation failed")
            else:
                resol = float(lines[0])
            self.resol = resol
            return True
        else:
            return False

    def writeResol(self, resol):
        # Check if the resolution calculation has been done or not
        resol_info_path = os.path.join(self.proc_path, self.resol_info)
        ofile = open(resol_info_path,"w")
        ofile.write("%5.2f\n" % resol)
        return True

    def writeFail(self):
        # Check if the resolution calculation has been done or not
        resol_info_path = os.path.join(self.proc_path, self.resol_info)
        ofile = open(resol_info_path,"w")
        ofile.write("FAILED\n")
        return True

    def get_resolution(self):
        if self.checkReady() == True:
            return self.resol

        resol = self.resol

        command = "yamtbx.python /oys/xtal/yamtbx/yamtbx/dataproc/auto/command_line/decide_resolution_cutoff.py %s"%self.xscalehkl_path
        logs = subprocess.Popen(
            command, stdout=subprocess.PIPE,
            shell=True).communicate()[0]

        lines = logs.split('\n')
        
        for line in lines:
            print "logline in ResolutionFromXscaleHKL",line
            if line.rfind("Suggested cutoff")!=-1:
                self.resol = float(line.split()[2])
        # Resolution cannot be got correctly
        if self.resol < 0.0:
            self.writeFail()
            raise MyException.GetResolutionFailed("ResolutionFromXscaleHKL: Resolution calculation failed")
        
        # Writing a resolution value to the .resol_dat
        self.writeResol(self.resol)

        return resol

if __name__ == "__main__":
    rfx = ResolutionFromXscaleHKL(sys.argv[1])
    print rfx.get_resolution()
