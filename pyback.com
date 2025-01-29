#!/bin/csh

find . -name '*.py' | xargs tar cvfz /isilon/BL32XU/TMP/200120-1400-isilon_honmono_PPPP.tgz --exclude="24.NABE"
#find . -name '*.py' 
