#!/bin/csh
# This script is written by K.Hirata
# Please inform me if you find bugs in this script
# 2006.11.30 K.Hirata e-mail:hirata@spring8.or.jp
#
# Version up on 20080511 by K.Hirata
# Version up on 20080523 by K.Hirata
# Version up on 2020/03/03 by K.Hirata
# -> ARPwARP model building cycle was added.
# -> Thanks to Dr. Makino
#
# What you must do
# Modify variants in the header of this script
# This script extracts cell parameters from 'merged' .sca file.
#

# Making scalepack script
# Parameters to be modified 
###################################################################
set SYMM='P43212'
set PROJECT='brsad'
set PHASE_MIN_RESOL=25
set NUM_OF_TRY=1000
set NUM_OF_FIND=3
set ANOM_ATOM=Br
set SOLVENT=0.40
set NUM_OF_DM=50
set NRESIDUES=118
set HKLFILE=xscale.hkl
set PHASE_MAX_RESOL=`yamtbx.python ~/PPPP/11.ClusterAnalysis/ResolutionFromXscaleHKL.py $HKLFILE`
set SEQ_FILE='/isilon/users/admin45/admin45/Scripts/lys.pir'
set AUTOBUILD=3
# End of parameters to be modified 
###################################################################

set CELL=`grep CELL $HKLFILE |grep -v ISET | awk '{print $2, $3, $4, $5, $6, $7}'`

### SHELX part ####
shelxc $PROJECT << eof |tee shelxc.log
SAD $HKLFILE
MAXM 20
FIND $NUM_OF_FIND
SFAC $ANOM_ATOM
NTRY $NUM_OF_TRY
cell $CELL
SPAG $SYMM
SHELL $PHASE_MIN_RESOL $PHASE_MAX_RESOL
eof

echo "SHELXC finished"

shelxd ${PROJECT}_fa |tee shelxd.log

echo "SHELXD finished"
SHELXE:
shelxe ${PROJECT} ${PROJECT}_fa -s${SOLVENT} -m${NUM_OF_DM} -a${AUTOBUILD} > shelxe_o.log
shelxe ${PROJECT} ${PROJECT}_fa -s${SOLVENT} -m${NUM_OF_DM} -a${AUTOBUILD} -i > shelxe_i.log
