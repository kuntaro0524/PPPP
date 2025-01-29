import os,sys,math,numpy, types

beamline = "BL32XU"

sys.path.append("/isilon/%s/BLsoft/PPPP/Libs/" % beamline.upper())
sys.path.append("/isilon/%s/BLsoft/PPPP/10.Zoo/Libs/" % beamline.upper())

import AttFactor
import MyException

class BSSmeasurementLog:
    def __init__(self, filename):
        self.bsslog = filename
        self.attfac = AttFactor.AttFactor()

        self.beam_shape = "NONE"
        self.wavelength = -9999.9999
        self.hbeam = -1
        self.vbeam = -1
        self.start_phi = 0.0
        self.end_phi = 90.0
        self.osc_width = 0.1
        self.total_osc = 10.0
        self.att_factor = -9999.9999
        self.exp_time = 0.02
        self.isPrep = False
        self.conds_dict = {}
        # Flag to detect 'advanced mode'
        self.isAdvanced = False

        """
 Sample  = Tray:CPS1416, Well:6
 FILE_NAME = /isilon/users/target/target/AutoUsers/200218/ariyoshi/CPS1416-06/data00//cry00_??????.h5
 starting_serial = 1
 JOB_MODE  = Crystal Check
 Beam shape = rectangle, Beam size = 15.0[um] x 10.0[um] (h x w)
 DETECTOR  = PAD (EIGER9M) :
 DATA COLLECTION_PARAMETERS :
  scan_from = -45.000[deg], scan_to = 315.000[deg], scan_step = 0.100[deg]
  sampling_interval = 1, number_of_images = 3600 x 1
  delay_time = 100.0[msec], cameralength = 210.6[mm], attenuator = Al 550um
  ver. offset = 0.0[mm], hor. offset = 0.0[mm]
  inverse_beam = no
  wavelength = 1.00000, expose_time = 0.020[sec]

 Advanced Centering Parameters
  mode = vector_centering, type = auto_step
  adv_npoint = 327, adv_step = 0.0006[mm], adv_interval = 11
  center #1:  0.3237 -10.1666 -1.2954
  center #2:  0.3025 -10.3466 -1.2954
        """

    ppp = "Beam shape = rectangle, Beam size = 15.0[um] x 10.0[um] (h x w)"
    def parseBeamsize(self, line):
        beam_index = 0
        cols = line.split(",")
        for col in cols:
            new_cols = col.split("=")
            if col.rfind("Beam shape") != -1:
                self.beam_shape = new_cols[1].strip()
            if col.rfind("Beam size") != -1:
                shape_str = new_cols[1]
                beams_str = shape_str.split("[um]")
                for bstr in beams_str:
                    ppp = bstr.split()
                    for p in ppp:
                        if p.replace(".","").isdigit() and beam_index == 0:
                            self.vbeam = float(p)
                            beam_index += 1
                        elif p.replace(".","").isdigit() and beam_index ==1:
                            self.hbeam = float(p)
                            beam_index += 1

        #print "Beam=", self.hbeam, self.vbeam

    ppp = "scan_from = -45.000[deg], scan_to = 315.000[deg], scan_step = 0.100[deg]"
    def parseScanConds(self, line):
        cols = line.split(",")
        #print "DDDDDDDDDDDDDDDDDDDDD=",cols
        index = 0
        for col in cols:
            #print col
            col2 = col.split("[deg]")
            for col3 in col2:
                val_str = col3[col3.rfind("=")+1:]
                if val_str.replace(".","").replace("-","").replace(" ","").isdigit() == True:
                    value = float(val_str)
                    if index == 0:
                        self.start_phi = value
                        index += 1
                    elif index == 1:
                        self.end_phi = value
                        index += 1
                    elif index == 2:
                        self.osc_width = value
                        index +=1
        self.total_osc = self.end_phi - self.start_phi

    def store2dict(self):
        if self.isPrep == False: self.prep()
        for key, value in zip(self.__dict__.keys(), self.__dict__.values()):
            if key == "conds_dict":
                continue
            self.conds_dict[key] = value

        return self.conds_dict

    def parseWL(self, line):
        cols = line.split(",")
        index = 0
        for col2 in cols:
            if col2.rfind("=") != -1:
                col3 = col2.split("=")
                for col4 in col3:
                    if col4.replace(".","").replace("-","").replace(" ","").isdigit() == True:
                        if index == 0:
                            self.wavelength = float(col4)
                            index += 1
                        elif index == 1:
                            self.exp_time = float(col4)
                            index += 1

    def prep(self):
        # BSS log flag
        isBSSlog = False
        lines = open(self.bsslog, "r").readlines()
        # Advanced flag
        # Attenuator
        for line in lines:
            # Beam shape
            if line.rfind("Beam shape") != -1:
                self.parseBeamsize(line)
            if line.rfind("scan_from") != -1:
                self.parseScanConds(line)
            if line.rfind("attenu") != -1:
                self.parseAttThick(line)
            if line.rfind("wavelength") != -1:
                self.parseWL(line)
            if line.rfind("Advanced Centering Parameters") != -1:
                self.isAdvanced = True
                self.readAdvancedSettings()
            if line.rfind("JOB_ID#") != -1:
                isBSSlog = True
        # check if this file is BSS log file
        if isBSSlog == False:
            raise MyException.NotBSSlog("This ain't a bss log. should be skipped.")

        self.isPrep = True
        self.getExpConds()
        return self.isPrep

    def readAdvancedSettings(self):
        lines = open(self.bsslog, "r").readlines()
        self.code_ds = []
        for line in lines:
            if line.rfind("mode =") != -1:
                if line.rfind("multiple_crystals") != -1:
                    self.mode = "multi"
                if line.rfind("vector_centering") != -1:
                    self.mode = "helical"
            if line.rfind("center #") != -1:
                code = []
                junk, number_str, xstr, ystr, zstr = line.split()
                cry_number = int(number_str.replace("#","").replace(":",""))
                code.append(float(xstr))
                code.append(float(ystr))
                code.append(float(zstr))
                self.code_ds.append((cry_number, code))

        #print self.mode

    def appendDict(self, key, param):
        try:
            self.conds_dict[key] = param
        except MyException.FailedToStoreDict as e:
            raise e

    def getExpConds(self):
        if self.isPrep == False:
            self.prep()

        if self.wavelength > 0.0:
            self.att_factor = self.attfac.calcAttFac(self.wavelength,self.att_thick,material="Al")
            #print "calculated att_factor=", self.att_factor
        else:
            self.att_factor = -9999.9999

        return self.start_phi, self.end_phi, self.osc_width, self.exp_time, self.att_factor

    def getWL(self):
        if self.isPrep == False:
            self.prep()
        return self.wavelength

    def getBeamsize(self):
        if self.isPrep == False:
            self.prep()
        return self.hbeam, self.vbeam

    def parseAttThick(self,line):
        idx = line.rfind("att")
        if idx != -1:
            cols = line[idx:].split()
            metal = cols[-2]
            thick_str = cols[-1]

            if thick_str == "None":
                self.att_thick = 0.0
            elif thick_str.rfind("um") != -1:
                self.att_thick = float(thick_str.replace("um",""))
            elif thick_str.rfind("mm") != -1:
                self.att_thick = float(thick_str.replace("mm",""))*1000.0

if __name__ == "__main__":
    bssml = BSSmeasurementLog(sys.argv[1])
    # return self.start_phi, self.end_phi, self.osc_width, self.exp_time, self.att_factor

    startphi, enphi, osc_width, exp_time, att_factor = bssml.getExpConds()
    wavelength = bssml.getWL()

    #print startphi, enphi, osc_width, exp_time, wavelength
    conds_dict = bssml.store2dict()

    #print conds_dict

    ham_string = "att_factor = %(att_factor).5f, %(exp_time).2f"% conds_dict
    print conds_dict
