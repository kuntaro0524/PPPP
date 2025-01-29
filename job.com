shelxc sad < sad_shelxc.in | tee shelxc.log
shelxd sad_fa.ins
sad sad_fa -m20 -s0.57 -l2 -d0.1 -e3.2 -h -b -a3 -q -i
sad sad_fa -m20 -s0.57 -l2 -d0.1 -e3.2 -h -b -a3 -q 
