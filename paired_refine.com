#!/bin/csh
set MODEL=~/170822-Conso/193l_prot.pdb
set SYMM=P43212
set LOWRES=1.5
set HIGHRES=1.1
set COLUMN="F"
yamtbx.python ~/PPPP/11.ClusterAnalysis/make_paired_refine_isotropic.py $MODEL $SYMM $LOWRES $HIGHRES $COLUMN
csh ./all.csh
