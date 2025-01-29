import sys,os,datetime,glob
import numpy

flist=glob.glob("./*.img")

n_image=len(flist)

tlist=[]
for file in flist:
	tmp_time=os.stat(file).st_mtime
	tlist.append(tmp_time)

ntimea=numpy.array(tlist)

maxt=ntimea.max()
mint=ntimea.min()

print "%5d images"%n_image
time_for_this_dir=maxt-mint
print "Time for data collection: %8.1f sec"%time_for_this_dir
print "Average time for each irradiation point: %8.3f sec"%(time_for_this_dir/float(n_image))
