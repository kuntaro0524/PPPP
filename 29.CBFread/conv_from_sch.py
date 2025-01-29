import sys,math,os
import ConvertHD5
from libtbx import easy_mp

if __name__ == "__main__":
        import sys

	sch_lines=open(sys.argv[1],"r").readlines()
        master_file=sys.argv[2]
	proc_list=[]


	ndata=0
	for line in sch_lines:
		if line.rfind("Advanced gonio coordinates")!=-1: 
			ndata+=1
		if line.rfind("Scan Condition")!=-1:
			#print cols
			cols=line.split()
			startphi=float(cols[2])
			endphi=float(cols[3])
			osc_width=float(cols[4])
			nframes=int((endphi-startphi)/osc_width)
			# 1deg summation
			nconv=int(1.0/osc_width)

	for nth_data in range(0,ndata):
		start_num_of_this_data=1
		center_n=int(nframes/2.0)
		start_num_of_this_data=nframes*nth_data+1
		start_num=start_num_of_this_data-int(nconv/2)
		end_num  =start_num_of_this_data+int(nconv/2)
		filename="cry_%03d_000001.cbf"%nth_data
		print start_num_of_this_data,start_num,end_num,filename
               	proc_list.append((master_file,start_num,end_num,filename))

        print "making %05d files"%len(proc_list)
        easy_mp.pool_map(fixed_func=lambda n: ConvertHD5.ConvertHD5(n).process(), args=proc_list, processes=8)

        command="tar cvfz cbf.tgz *.cbf"
        os.system(command)
        command="\\rm -Rf *.cbf"
        os.system(command)
