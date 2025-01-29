#!/bin/csh
a2ps $1 -o $2.ps
ps2pdf $2.ps 
\rm -rf $2.ps
