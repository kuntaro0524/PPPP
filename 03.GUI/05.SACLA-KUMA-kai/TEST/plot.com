gnuplot  -p << eof 
splot "l" i 0 u 1:2:3  , \
"" i 1 u 1:2:3 , \
"" i 2 u 1:2:3 , \
"" i 3 u 1:2:3 , \
"" i 4 u 1:2:3 , \
"" i 5 u 1:2:3 , \
"" i 6 u 1:2:3
eof
