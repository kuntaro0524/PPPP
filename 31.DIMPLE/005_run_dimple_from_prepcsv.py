import os, sys, math, logging, csv, glob
#sys.path.append("/isilon/BL32XU/BLsoft/PPPP/10.Zoo/Libs")
sys.path.append("/isilon/BL32XU/BLsoft/PPPP/Libs")
import MyException
import Xds2Mtz
import ResolutionFromXscaleHKL
import ComRefine
import logging.config

beamline = "BL32XU"

if __name__ == "__main__":
    lines = open(sys.argv[1],"r").readlines()

    # Logging setting
    logname = "./proc_dimple.log"
    logging.config.fileConfig('/isilon/%s/BLsoft/PPPP/10.Zoo/Libs/logging.conf' % beamline, defaults={'logfile_name': logname})
    logger = logging.getLogger('Proc_DIMPLE')

    n_process = 0
    ref_refl = ""
    # read lines and stores information

    for line in lines[1:]:
        #logger.info("LIST:%s" % line,)
        logger.info("########### Processing started #############################")
        cols = line.split(',')
        if len(cols) != 5:
            logging.info("This line is not suitable for process. %s ncols = %5d"% (line, len(cols)))
        else:
            puck_pin,sample_name, refl_name, model_name, symm = line.split(',')
            symm = symm.strip()
            logging.info("puck_pin= %s" %(puck_pin))
            logging.info("sample= %s" %(sample_name))
            logging.info("refl_name=%s" % refl_name) 
            logging.info("model_name=%s" % model_name) 
            logging.info("symm=%s" % symm) 

            # Preparation
            proc_dir = refl_name[:refl_name.rfind("/")]
            logging.info("reflection file directory: %s" % proc_dir)
            dimple_dir = os.path.join(proc_dir,"dimple")
            logging.info("DIMPLE directory: %s" % dimple_dir)

            # making a DIMPLE directory
            if os.path.exists(dimple_dir) == False:
                os.makedirs(dimple_dir)
                logging.info("making DIMPLE directory: %s" % dimple_dir)

            # convert XDS reflection to MTZ file
            xds2mtz = Xds2Mtz.Xds2Mtz(refl_name)
            logging.info("File converting from %s with spacegroup = %s" % (refl_name, symm))
            xds2mtz.setSPG(symm)

            if n_process == 0:
                logging.info("This file will be a reference file for common Free-R flags")
                xds2mtz.addFreeRflag()
            else:
                logging.info("A reference Free-R flag file: %s" % ref_refl)
                xds2mtz.setReferenceFlagFile(ref_refl)

            # output directory can be defined
            xds2mtz.runXDS2MTZ(dimple_dir)

            # prefix of an input reflection file
            only_filename = refl_name[refl_name.rfind("/")+1:]
            prefix_of_refl = only_filename.replace(".HKL","").replace(".hkl","")
            
            logging.info("reflection file = %s" % only_filename)
            logging.info("a prefix of reflection file = %s" % prefix_of_refl)
            # check if the reflection file exists
            # xds2mtz.py only output a reflection file with the same prefix of input .HKL file 
            mtz_name = "%s.mtz" % prefix_of_refl
            mtz_file_path = os.path.join(dimple_dir, mtz_name)

            if n_process == 0:
                n_process += 1
                ref_refl = mtz_file_path

            if os.path.exists(mtz_file_path) == False:
                logging.error("%s does not exist." % mtz_file_path)
            else:
                # Checking file paths
                if os.path.exists(model_name) == False:
                    print "%s does not exist" % model_name
            
                # Resolution calculation from XDS_ASCII.HKL
                resol_calculator = ResolutionFromXscaleHKL.ResolutionFromXscaleHKL(refl_name)

                try:
                    dmin = resol_calculator.get_resolution()
                except MyException.GetResolutionFailed as e:
                    logging.error("Exception in resolution estimation from HKL file. %s" % e.args)
                    logging.error("Data analysis is skipped for this dataset")

                    continue
            
                # Do dimple refinement
                comf = ComRefine.ComRefine(dimple_dir)
                comname = comf.dimpleSimple(mtz_name,symm,dmin,model_name,sample_name)
                logging.info("Submitting the job to SGE: %s " % comname)
                os.system("qsub %s" % comname)
                logging.info("Now calculating... %s " % comname)
