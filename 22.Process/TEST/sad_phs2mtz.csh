#!/bin/csh -f
# 
# Shell script for converting phs to mtz-format 
# This script was written by HKL2MAP 0.3.i-beta
# f2mtz keeps order of columns
# cad picks up things in a different order and then writes E1...E4
# 
# To convert from phs to mtz type: 
#    ./sad_phs2mtz.csh <name>.phs 
# 
set fname = $1:r
f2mtz hklin ${fname}.phs hklout t_tmp.mtz > t_f2mtz.log <<END
CELL 78.9 78.9 37.22 90 90 90 
SYMM P43212 
LABOUT H K L FP FOM PHIB SIGFP
CTYPOUT H H H F W P Q
END
# 
cad hklin1 t_tmp.mtz hklout $fname.mtz > t_cad.log <<eof-cad
LABIN FILE 1 E1=FP E2=SIGFP E3=PHIB E4=FOM
LABOUT E1=FP E2=SIGFP E3=PHIB E4=FOM
eof-cad
