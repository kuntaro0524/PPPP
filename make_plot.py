import pylab 
import numpy
import glob

files=glob.glob("./*csv")

plot_list=[]
for f in files:
	dsa=[]
	ccha=[]
	isigia=[]
	rsyma=[]

	dataname=f.replace(".csv","")
	lines=open(f,"r").readlines()
	for line in lines:
		if line.rfind("#")!=-1:
			continue
		cols=line.split(",")
		dstar=float(cols[1])
		cch=float(cols[4])
		isigi=float(cols[3])
		r=float(cols[2])

		dsa.append(dstar)
		ccha.append(cch)
		isigia.append(isigi)
		rsyma.append(r)

	ndsa=numpy.array(dsa)
	nccha=numpy.array(ccha)
	nsigi=numpy.array(isigia)

	plot_list.append((dataname,ndsa,nccha,nsigi))


# CC1/2 plot
for each_data in plot_list:
	dname,ndsa,nccha,nsigi=each_data
	pylab.plot(ndsa,nccha,"o-",label=dname)
	pylab.legend(loc='lower left',fontsize=5)

pylab.savefig("cch.png")
pylab.clf()

for each_data in plot_list:
	dname,ndsa,nccha,nsigi=each_data
	pylab.yscale("log")
	pylab.plot(ndsa,nsigi,"o-",label=dname)
	pylab.legend(fontsize=5)

pylab.savefig("isigi.png")
