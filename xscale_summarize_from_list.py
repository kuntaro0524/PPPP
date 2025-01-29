import os,sys
import time
sys.path.append("/isilon/BL32XU/BLsoft/PPPP/")
import DirectoryProc
import glob
import numpy
import pylab
import AnaCORRECT

lstfile=sys.argv[1]
filelist=open(lstfile,"r").readlines()

ofile=open("dum","a")

file_index=0
for eachname in filelist:
	# PREFIX GET
	cols=eachname.strip().split('/')
	print cols
	nrun=cols[len(cols)-2]
	ncluster=cols[len(cols)-3]
	prefix="%s-%s"%(ncluster,nrun)
	ofile=open("%s.csv"%prefix,"w")
	filepath=os.path.abspath(eachname).strip()
	ac=AnaCORRECT.AnaCORRECT(filepath)
	ofile.write("# %s\n"%filepath)
	for logstr in ac.readLog():
		ofile.write("%s"%logstr)
	file_index+=1
	ofile.close()

time.sleep(10)
files=glob.glob("./*csv")

print files

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
        pylab.legend(loc='lower left',fontsize=10)

pylab.savefig("cch.png")
pylab.clf()

for each_data in plot_list:
        dname,ndsa,nccha,nsigi=each_data
        pylab.yscale("log")
        pylab.plot(ndsa,nsigi,"o-",label=dname)
        pylab.legend(fontsize=10)

pylab.savefig("isigi.png")
