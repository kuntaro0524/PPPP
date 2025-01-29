#!/bin/csh
foreach FILE(`ls *.ppm`)
set PREFIX=`echo $FILE | sed 's/.ppm/.png/'`
convert $FILE $PREFIX.png
end
