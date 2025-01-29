import os,sys,numpy,scipy
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid.parasite_axes import SubplotHost

time_raws=[]
shut_raws=[]
xray_raws=[]
eiger_raws=[]
yenc_raws=[]

############################
# FILE CONVERTER
############################
def extract_info(csvfile):
	infile=open(csvfile,"r")
	lines=infile.readlines()
	infile.close()
	
	# Shutter open voltage ~3.4V
	skip_head=10

	idx=0
	for line in lines[skip_head:]:
        	cols=line.split(",")
		time_raws.append(float(cols[0]))
		shut_raws.append(float(cols[1]))
       		xray_raws.append(float(cols[2]))
        	eiger_raws.append(float(cols[3]))
        	yenc_raws.append(float(cols[4]))

	return time_raws,shut_raws,xray_raws,eiger_raws,yenc_raws

############################
def find_eiger_open_close(eiger_array):
	# IDOU HEIKIN N points
	n=10
	neiger=numpy.array(eiger_array)
	# Find shutter open close
	idx=0
	array=[]
	start_around_value=[]
	start_around_index=[]
	end_around_value=[]
	end_around_index=[]
	
	# Find the starting point
	open_flag=False
	close_flag=False
	
	opentime_array=[]
	closetime_array=[]
	for d in neiger:
        	if open_flag==True and d < 1.0:
                	closetime_array.append(idx)
                	open_flag=False
        	if open_flag==False and d > 3.0:
                	opentime_array.append(idx)
                	open_flag=True
        	idx+=1

	return opentime_array,closetime_array

###########################

############################
def find_xray_open_close(xray_array):
        # IDOU HEIKIN N points
        n=10
        nxray=numpy.array(xray_array)
        # Find shutter open close
        idx=0
        array=[]
        start_around_value=[]
        start_around_index=[]
        end_around_value=[]
        end_around_index=[]

        # Find the starting point
        open_flag=False
        close_flag=False

        opentime_array=[]
        closetime_array=[]
        for d in nxray:
                if open_flag==True and d < 0.5:
                        closetime_array.append(idx)
                        open_flag=False
                if open_flag==False and d > 0.5:
                        opentime_array.append(idx)
                        open_flag=True
                idx+=1

        return opentime_array,closetime_array

###########################


# This routine calculates Open/Close signals
def find_open_close(rawdata,max_thresh,min_thresh,smooth=False):

	nraw=numpy.array(rawdata)
	n=10

	# Idouheikin
	if smooth==True:
		smoothed=numpy.convolve(nraw,numpy.ones(n)/float(n),'same')
		grad=numpy.gradient(smoothed)
	else:
		grad=numpy.gradient(nraw)
		
	print "# NData=",len(nraw)
	print "# GRAD =",len(grad)

	# Find shutter open close
	line_index=0
	# To find the peak point around the opening point
	start_around_value=[]
	start_around_index=[]
	# To find the peak point around the closing point
	end_around_value=[]
	end_around_index=[]

	# Find the starting point
	open_flag=False
	close_flag=False

	opentime_array=[]
	closetime_array=[]

	# In differentiative curve
	# Finding + peak for open, - peak for close
	for g in grad:
		if g > max_thresh:
			start_around_value.append(g)
			start_around_index.append(line_index)
			open_flag=True
		if open_flag==True and g <= max_thresh:
			npa=numpy.array(start_around_value)
			max_index=numpy.argmax(npa)
			open_time=start_around_index[max_index]
			# Initializing the parameters
			open_flag=False
			start_around_value=[]
			start_around_index=[]
			# Open time is stored
			opentime_array.append(open_time)
		if g < min_thresh:
			close_flag=True
			end_around_index.append(line_index)
			end_around_value.append(g)
		if close_flag==True and g >= min_thresh:
			npa=numpy.array(end_around_value)
			max_index=numpy.argmin(npa)
			close_time=end_around_index[max_index]
			# Initializing the parameters
			close_flag=False
			end_around_value=[]
			end_around_index=[]
			# Close time is stored
			closetime_array.append(close_time)
		line_index+=1

	return opentime_array,closetime_array,grad

######################   MAIN
csvfile=sys.argv[1]
time_raws,shut_raws,xray_raws,eiger_raws,yenc_raws=extract_info(csvfile)

eo,ec=find_eiger_open_close(eiger_raws)
so,sc,splot= find_open_close(shut_raws,1.0,-1.0,smooth=False)
xo,xc=find_xray_open_close(xray_raws)

# LOG FILE
prefix=csvfile[csvfile.rfind("/")+1:].replace(".csv","")
logname="%s.log"%prefix
logfile=open(logname,"w")

# number of measurements
nmeas=len(so)
npoints_in_line=int(len(eo)/nmeas)

logfile.write("# Measurement         : %5d\n"%nmeas)
logfile.write("# of points in line   : %5d\n"%npoints_in_line)

def calc_time(basetime,targettime):
	diff=targettime-basetime
	unit_change=diff*1E-6 #[sec]
	return unit_change

logparams=[]
for nm in range(0,nmeas):
	# X-ray open index
	i_xopen=xo[nm]
	y_xopen=yenc_raws[i_xopen]
	t_xopen=time_raws[i_xopen]

	# the first index for each line
        i0=nm*npoints_in_line

	# EIGER start point
	i_eiger_start=eo[i0]
	y_eiger_start=yenc_raws[i_eiger_start]
	t_eiger_start=time_raws[i_eiger_start]-t_xopen

	# EIGER end point
	# EIGER end point
	i1=i0+npoints_in_line-1
	#print "INDEX: %5d%5d%5d"%(i_xopen,i0,i1)
	i_eiger_end=ec[i1]
	y_eiger_end=yenc_raws[i_eiger_end]
	t_eiger_end=time_raws[i_eiger_end]-t_xopen

	# X-ray close index
	i_xclose=xc[nm]
	y_xclose=yenc_raws[i_xclose]
	t_xclose=time_raws[i_xclose]-t_xopen

	# Travel length
	tlength=numpy.fabs(y_eiger_end-y_eiger_start)

	# Travel length between from 'EIGER close' to 'Shutter close'
	length_res=numpy.fabs(y_xclose-y_eiger_end)
	# Travel length between from 'Shutter open' to 'EIGER open'
	diff_start=numpy.fabs(y_eiger_start-y_eiger_end)

	# The first line
	if nm==0:
		ystart=y_eiger_start
	if nm==1:
		yend=y_eiger_end
		diff=numpy.fabs(yend-ystart)

	logfile.write("XO %12.5f ES(%9.4f,%9.4f) EE(%9.4f,%9.4f),XC(%9.4f,%9.4f) TRAVEL=%9.4f RES(start,end)=(%9.4f,%9.4f)\n"%(\
		y_xopen,t_eiger_start,y_eiger_start,t_eiger_end, \
		y_eiger_end,t_xclose,y_xclose,tlength,diff_start,length_res))
	logparams.append((t_xopen,y_xopen,t_eiger_start,y_eiger_start,t_eiger_end,y_eiger_end,t_xclose,y_xclose,tlength,length_res))

logfile.write("GO_WAY START %9.4f /BACK_WAY %9.4f DIFF= %9.4f\n"%(ystart,yend,diff))
logfile.write("Residual travel + diff(GO,BACK) = %9.4f\n"%(diff+length_res))

for s in so:
	logfile.write("#shutter open  %10d\n"%s)
for x in xc:
	logfile.write("#shutter close %10d\n"%x)
for e in eo:
	logfile.write("#EIGER open    %10d\n"%e)
for e in ec:
	logfile.write("#EIGER close   %10d\n"%e)

logfile.close()

# Writing new csv file for plotting
offset=2000
measure_index=0
for so_index,xc_index in zip(so,xc):
        divided_csv="%s_%03d.csv"%(prefix,measure_index)
        divided_png="%s_%03d.png"%(prefix,measure_index)
        dcsv=open(divided_csv,"w")

        for idx in range(so_index-offset,xc_index+offset):
                dcsv.write( "%12.5f %12.5f %12.5f %12.5f %12.5f\n"%(\
                        time_raws[idx],
                        shut_raws[idx],
                        xray_raws[idx],
                        eiger_raws[idx],
                        yenc_raws[idx]))
        dcsv.close()
        start_i=so_index-offset
        end_i=xc_index+offset
        plot_t=numpy.array(time_raws[start_i:end_i])
        plot_s=numpy.array(shut_raws[start_i:end_i])
        plot_e=numpy.array(eiger_raws[start_i:end_i])
        plot_x=numpy.array(xray_raws[start_i:end_i])
        plot_y=numpy.array(yenc_raws[start_i:end_i])

        # PREPARATION
        fig=plt.figure(figsize=(20,10))
        host=SubplotHost(fig,111)
        fig.add_subplot(host)
        par=host.twinx()

        # PREPARE GRAPHS
        p1=par.plot(plot_t,plot_s,'-',color="r",label="Shutter signal")
        p2=par.plot(plot_t,plot_e,'-',color="g",label="EIGER Ext.")
        p3=par.plot(plot_t,plot_x,'-',color="m",label="X-ray intensity")
        p4=host.plot(plot_t,plot_y,'-',color="c",label="Y Encoder")

        plt.subplots_adjust(right=0.6)
        host.legend()
        host.legend(bbox_to_anchor=(1.10,1),loc='upper left',borderaxespad=0)
        host.legend(bbox_to_anchor=(1.10,0.7),loc='upper left',borderaxespad=0)

        # Text results
        t_xopen,y_xopen,t_eiger_start,y_eiger_start,t_eiger_end,y_eiger_end,t_xclose,y_xclose,tlength,length_res=logparams[measure_index]
	at_eiger_start=t_xopen+t_eiger_start
	at_eiger_end=t_xopen+t_eiger_end
	at_xclose=t_xopen+t_xclose

        host.text(t_xopen,y_xopen,"%8.5f"%y_xopen,color="m")
        host.text(at_eiger_start,y_eiger_start,"%8.5f"%y_eiger_start,color="g")
        host.text(at_eiger_end,y_eiger_end,"%8.5f"%y_eiger_end,color="g")
        host.text(at_xclose,y_xclose,"%8.5f"%y_xclose,color="m")
	host.set_xlabel("Time[sec]")
	diff_start=y_eiger_start-y_xopen
        host.set_title("Length(EO->EC)=%8.5f Length(XO->EO)=%8.5f Length(EC->XC)=%8.5f"%(tlength,diff_start,length_res))
        #fig.show()
        fig.savefig(divided_png)
        #plt.clf()

        measure_index+=1
