import os,sys
import time
sys.path.append("/isilon/BL32XU/BLsoft/PPPP/")
import DirectoryProc
import glob
import numpy
import pylab
import AnaCORRECT

csv_list=glob.glob("*.csv")

file_index=0
csv_table=[]

for csvfile in csv_list:
	da=[]
	ds2a=[]
	ra=[]
	isa=[]
	ccha=[]
	lines=open(csvfile,"r").readlines()
	for line in lines:
		cols=line.strip().split(",")
		if len(cols)>1:
			da.append(float(cols[0]))
			ds2a.append(float(cols[1]))
			ra.append(float(cols[2]))
			isa.append(float(cols[3]))
			ccha.append(float(cols[4]))
	nda=numpy.array(da)
	nds2a=numpy.array(ds2a)
	nra=numpy.array(ra)
	nisa=numpy.array(isa)
	nccha=numpy.array(ccha)
	# filename -> number of datasets
	iii=csvfile.rfind("sets")
	ndata=int(csvfile[:iii])
	csv_table.append((ndata,csvfile,nda,nds2a,nra,nisa,nccha))

csv_table.sort(key=lambda x:int(x[0]))

pylab.yscale("log")
for each_data in csv_table:
        ndata,dname,nda,nds2a,nra,nisa,nccha=each_data
	comment="%4d sets"%ndata
        pylab.plot(nds2a,nisa,"o-",label=comment)
        pylab.legend(loc='upper right',fontsize=15)
	pylab.xlabel("1/resolution**2")
	pylab.ylabel("<I/sigI>")

pylab.savefig("ndata_isigi_plot.png")
pylab.clf()

for each_data in csv_table:
        ndata,dname,nda,nds2a,nra,nisa,nccha=each_data
	comment="%4d sets"%ndata
        pylab.plot(nds2a,nccha,"o-",label=comment)
        pylab.legend(loc='lower left',fontsize=15)
	pylab.xlabel("1/resolution**2")
	pylab.ylabel("CC(1/2)")

pylab.savefig("ndata_cchalf.png")
pylab.clf()

for each_data in csv_table:
        ndata,dname,nda,nds2a,nra,nisa,nccha=each_data
	comment="%4d sets"%ndata
        pylab.plot(nds2a,nra,"o-",label=comment)
        pylab.legend(loc='upper left',fontsize=15)
	pylab.xlabel("1/resolution**2")
	pylab.ylabel("Rmeas")

pylab.savefig("ndata_rmeas.png")
pylab.clf()
