import os,sys,math
import BeamsizeConfig
sys.path.append("/isilon/BL32XU/BLsoft/PPPP/")

import Fitting
import AnaDSlog

if __name__ == "__main__":
    import sys

    config_dir="/isilon/BL32XU/BLsoft/PPPP/10.Zoo/ZooConfig/"
    an=AnaDSlog.AnaDSlog(sys.argv[1])
    bsc=BeamsizeConfig.BeamsizeConfig(config_dir)

    hbeam,vbeam=an.getBeamsize()
    beam_index,flux_factor,flux=bsc.getBeamParams(hbeam,vbeam)

    logstr=an.prepSimple(flux)
    for log in logstr:
	print "%s,"%log,
