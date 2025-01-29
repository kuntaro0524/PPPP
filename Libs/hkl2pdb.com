#!/bin/csh
#$ -cwd
#$ -o /isilon/BL32XU/BLsoft/PPPP/Libs
#$ -e /isilon/BL32XU/BLsoft/PPPP/Libs
setenv PHENIX_OVERWRITE_ALL true
shelxc lys << eof > shelxc.log
SAD xscale.hkl
MAXM 20
FIND 12
SFAC S
NTRY 10
cell   78.000   78.000   36.000   90.000   90.000   90.000
SPAG P43212
SHELL 25.00  1.80
eof

shelxd lys_fa > shelxd.log

SHELXE:
shelxe lys lys_fa -s0.40 -m50 -a5 > shelxe_o.log
shelxe lys lys_fa -s0.40 -m50 -a5 -i > shelxe_i.log
