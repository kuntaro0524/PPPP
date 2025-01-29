import os,sys,numpy,scipy
import matplotlib.pyplot as plt

############################
# Extracting information
############################
def extract_info(csvfile):
	# Data array
	time_raws=[]
	shut_raws=[]
	xray_raws=[]
	eiger_raws=[]
	yenc_raws=[]

	infile=open(csvfile,"r")
	lines=infile.readlines()
	infile.close()
	
	# Shutter open voltage ~3.4V
	skip_head=10
	
	idx=0
	for line in lines[skip_head:]:
        	cols=line.strip().split(",")
		#print cols
		time_raws.append(float(cols[0]))
       		shut_raws.append(float(cols[1]))
        	xray_raws.append(float(cols[2]))
        	eiger_raws.append(float(cols[3]))
        	yenc_raws.append(float(cols[4]))

	#print len(time_raws)
	
	return time_raws,shut_raws,xray_raws,eiger_raws,yenc_raws

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

#############################################
############### MAIN
#############################################
csvfile=sys.argv[1]
time_raws,shut_raws,xray_raws,eiger_raws,yenc_raws=extract_info(csvfile)

prefix=csvfile[csvfile.rfind("/")+1:].replace(".csv","")
logname="%s.log"%prefix
logfile=open(logname,"w")

so,sc,splot= find_open_close(shut_raws,1.0,-1.0,smooth=False)
xo,xc=find_xray_open_close(xray_raws)

# number of measurements
nmeas=len(so)
logfile.write( "# Measurement         : %5d\n"%nmeas)

# Writing new csv file for plotting
measure_index=0
for so_index,xc_index in zip(so,xc):
	divided_csv="%s_%03d.csv"%(prefix,measure_index)
	divided_png="%s_%03d.png"%(prefix,measure_index)
	dcsv=open(divided_csv,"w")

	for idx in range(so_index,xc_index):
		dcsv.write( "%12.5f %12.5f %12.5f %12.5f %12.5f\n"%(\
			time_raws[idx],
			shut_raws[idx],
			xray_raws[idx],
			eiger_raws[idx],
			yenc_raws[idx]))
	dcsv.close()
	start_i=so_index-1000
	end_i=xc_index+1000
	plot_t=numpy.array(time_raws[start_i:end_i])
	plot_s=numpy.array(shut_raws[start_i:end_i])
	plot_e=numpy.array(eiger_raws[start_i:end_i])
	plot_x=numpy.array(xray_raws[start_i:end_i])
	plot_y=numpy.array(yenc_raws[start_i:end_i])
	measure_index+=1
	fig,ax1=plt.subplots()
	# x axis
	ax2=ax1.twinx()
	p1=ax1.plot(plot_t,plot_s,'-',label="Shutter open signal")
	p2=ax1.plot(plot_t,plot_e,'-',label="EIGER external")
	p3=ax1.plot(plot_t,plot_x,'-',label="X-ray intensity")
	p4=ax2.plot(plot_t,plot_y,'-',label="Encoder Y")
	p=[p1,p2,p3,p4]
	#ax1.legend(p,[i.get_label() for i in p])
	ax1.legend(bbox_to_anchor=(1.05,1),loc='upper left',borderaxespad=0)
	ax2.legend(bbox_to_anchor=(1.05,0.7),loc='upper left',borderaxespad=0)
	plt.subplots_adjust(right=0.7)
	#ax2.legend()

	plt.savefig(divided_png)
	plt.clf()

#logfile.write( "DIFF START %9.4f /END %9.4f points= %9.4f\n"%(ystart,yend,diff))
#logfile.write( "Residual travel + diff(GO,BACK) = %9.4f\n"%(diff+length_res))
