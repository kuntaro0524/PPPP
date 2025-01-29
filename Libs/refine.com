#!/bin/csh
#$ -wd /isilon/BL32XU/BLsoft/PPPP/Libs
#$ -o /isilon/BL32XU/BLsoft/PPPP/Libs
#$ -e /isilon/BL32XU/BLsoft/PPPP/Libs
setenv PHENIX_OVERWRITE_ALL true
copy_free_R_flag.py -r foo/reference.mtz /isilon/BL32XU/BLsoft/PPPP/Libs/ccp4/xscale.mtz -o /isilon/BL32XU/BLsoft/PPPP/Libs/free_common.mtz

dimple ccp4/xscale.mtz foo/model.pdb