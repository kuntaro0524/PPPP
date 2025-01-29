#!/bin/csh

echo $1

gnuplot --persist << eof
#set terminal png
#set output "$1.png"
unset label
set xrange[-1:1]
set yrange[-1:1]
set zrange[-1:1]
splot "test3.log" i $1 u 2:3:4 w l
eof
