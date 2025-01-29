#!/bin/csh
\rm -f Libs/*pyc ?
\rm -f Libs/*png 
\rm -f Libs/*jpg 
\rm -f Libs/core*

# CentOS7
#git add --ignore-removal ./KAMO/ ./*.py *zoo*sh Libs/ ./ZooConfig/bss/ ./ZooConfig/header/ LargeHolder/*.py *.com *.sh *.csh ./*txt ZOOGUI/*.py

# CentOS6
git add `find . -name '*.py'` 
git add `find . -name '*.com'`
git add `find . -name '*sh'`
git add `find . -name '*.csh'` 
git add ZOOGUI/ KUMAGUI/
