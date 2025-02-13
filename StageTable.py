import sys,os
import numpy as np
from Stage import *

def average(en_list,param):
	tmp_lower=[]
	tmp_upper=[]

	idx=0
        for en in en_list:
                if en < 10.0:
                        tmp_lower.append(param[idx])
                elif en >= 10.0:
                        tmp_upper.append(param[idx])

                idx+=1

        low_list =np.array(tmp_lower)
        high_list=np.array(tmp_upper)

	ave_low=low_list.mean()
	ave_high=high_list.mean()

	return ave_low,ave_high

if __name__=="__main__":

class StageTable:
	
	self __init__(self,server):
		self.stage=Stage(s)
		filename="/blconfig/bl41xu/bl41xu.config.template"
		tblfile="/isilon/BL32XU/BLsoft/PPPP/08.DynamicTable/140414.tbl"

	self 
	
		ifile=open(filename,"r")
		conf_lines=ifile.readlines()
	
		tfile=open(tblfile,"r")
	
	data=np.loadtxt(tblfile)
	
	#print data[1,:],data[:,1]
	en_list=data[:,0]
	stz_list=data[:,2]
	col_list=data[:,4]

	
	stz_LE,stz_HE=average(en_list,stz_list)
	diff_stz = stz_HE - stz_LE

	col_LE,col_HE=average(en_list,col_list)
	diff_colz = col_HE/2000.0 - col_LE/2000.0

	#print diff_colz

	sty_curr=stage.getYmm()
	stz_curr=stage.getZmm()
	
	stz_lines=""
	col_lines=""
	bs_lines=""
	for en in np.arange(8.0,9.5,0.5):
		if en < 10.0:
			line="st1_stage_1:%8.4f %8.5f %8.5f\n"%( en,sty_curr,stz_curr-diff_stz)
			stz_lines+=line
			line="col_offset:%8.4f %8.5f\n"%( en,0-diff_colz)
			col_lines+=line
			line="bs_offset:%8.4f %8.5f\n"%( en,0-diff_colz)
			bs_lines+=line
		else:
			line="st1_stage_1:%8.4f %8.5f %8.5f\n"%( en,sty_curr,stz_curr)
			stz_lines+=line
			line="col_offset:%8.4f %8.5f \n"%( en,0.0)
			col_lines+=line
			line="bs_offset:%8.4f %8.5f\n"%( en,0.0)
			bs_lines+=line

	for en in np.arange(9.5,10.5,0.1):
		if en < 10.0:
			line="st1_stage_1:%8.4f %8.5f %8.5f\n"%( en,sty_curr,stz_curr-diff_stz)
			stz_lines+=line
			line="col_offset:%8.4f %8.5f\n"%( en,0-diff_colz)
			col_lines+=line
			line="bs_offset:%8.4f %8.5f\n"%( en,0-diff_colz)
			bs_lines+=line
		else:
			line="st1_stage_1:%8.4f %8.5f %8.5f\n"%( en,sty_curr,stz_curr)
			stz_lines+=line
			line="col_offset:%8.4f %8.5f \n"%( en,0.0)
			col_lines+=line
			line="bs_offset:%8.4f %8.5f\n"%( en,0.0)
			bs_lines+=line

	for en in np.arange(10.5,25.0,1.0):
		if en < 10.0:
			line="st1_stage_1:%8.4f %8.5f %8.5f\n"%( en,sty_curr,stz_curr-diff_stz)
			stz_lines+=line
			line="col_offset:%8.4f %8.5f\n"%( en,0-diff_colz)
			col_lines+=line
			line="bs_offset:%8.4f %8.5f\n"%( en,0-diff_colz)
			bs_lines+=line
		else:
			line="st1_stage_1:%8.4f %8.5f %8.5f\n"%( en,sty_curr,stz_curr)
			stz_lines+=line
			line="col_offset:%8.4f %8.5f \n"%( en,0.0)
			col_lines+=line
			line="bs_offset:%8.4f %8.5f\n"%( en,0.0)
			bs_lines+=line

	print stz_lines
	print col_lines
	print bs_lines

	ofile=open("/isilon/BL32XU/bl41xu.config","w")

	for line in conf_lines:
		line=line.replace("ST_TABLE",stz_lines)
		line=line.replace("BSTABLE",bs_lines)
		line=line.replace("COLTABLE",col_lines)
		ofile.write("%s"%line)

	ofile.close()
