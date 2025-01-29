import os,sys,math,numpy,glob
sys.path.append("/isilon/BL32XU/BLsoft/PPPP")
from libtbx import easy_mp
import ConvertHD5
import DirectoryProc

class ResultsZOO:
    def __init__(self,datadir):
        self.datadir=datadir

    def getConditions(self,schfile):
        sch_lines=open(schfile,"r").readlines()
        for line in sch_lines:
            print line
            if line.rfind("Advanced gonio coordinates")!=-1:
                ndata+=1
            if line.rfind("Scan Condition")!=-1:
                cols=line.split()
                startphi=float(cols[2])
                endphi=float(cols[3])
                osc_width=float(cols[4])
                nframes=int((endphi-startphi)/osc_width)
                # 1deg summation
                nconv=int(1.0/osc_width)

        return startphi,endphi,osc_width,nframes

    def procAll(self):
        sch_files="*sch"
        sch_list=glob.glob(self.datadir+"/*sch")

        cols=""
        for schfile in sch_list:
            startphi,endphi,osc_width,nframes=self.conditions(schfile)
            print cols,startphi,endphi,osc_width,nframes

    def getScheudlePaths(self):
        dp=DirectoryProc.DirectoryProc(self.datadir)
        #findTargetFileInTargetDirectories(self,string_in_dire,string_in_filename,exclude_str=""):
        sch_files,sch_paths=dp.findTargetFileInTargetDirectories("data","sch","_kamoproc")

        return sch_files,sch_paths

    def getDataInfo(self,sch_file):
        sch_lines=open(sch_file,"r").readlines()
        n_multi=0
        for line in sch_lines:
            if line.rfind("Advanced gonio coordinates")!=-1:
                n_multi+=1
            if line.rfind("Scan Condition")!=-1:
                cols=line.split()
                startphi=float(cols[2])
                endphi=float(cols[3])
                osc_width=float(cols[4])
                nframes=int((endphi-startphi)/osc_width)
                # 1deg summation
                nconv=int(1.0/osc_width)
            if line.rfind("Sample Name:")!=-1:
                prefix=line.replace("Sample Name:","").strip()
            
        print prefix,n_multi,startphi,endphi,osc_width,nframes
        return prefix,n_multi,startphi,endphi,osc_width,nframes,nconv

    def procMultiDS(self,sch_file,sch_path):
        sch_lines=open(sch_file,"r").readlines()
        prefix,n_multi,startphi,endphi,osc_width,nframes,nconv=self.getDataInfo(sch_file)

        master_file=os.path.join(sch_path,"%s_master.h5"%prefix)

        proc_list=[]
        jpgfile_list=[]

        print "N_MULTI=",n_multi
        for nth_data in range(0,n_multi):
                center_n=int(nframes/2.0)
                start_num_of_this_data=nframes*nth_data+1
                center_of_rotation=start_num_of_this_data+center_n
            
                conv_startnum=center_of_rotation-int(nconv/2)
                conv_endnum  =center_of_rotation+int(nconv/2)

                filename="%s/multi_check_%03dth_%05d-%05d.cbf"%(self.datadir,nth_data,conv_startnum,conv_endnum)
                proc_list.append((master_file,conv_startnum,conv_endnum,filename))

        print proc_list
        print "making %5d files"%len(proc_list)
        jpgfile_list.append(easy_mp.pool_map(fixed_func=lambda n: ConvertHD5.ConvertHD5(n).process(), args=proc_list, processes=20))

        print jpgfile_list

    def procHelical(self,sch_file,sch_path):
        sch_lines=open(sch_file,"r").readlines()
        prefix,n_multi,startphi,endphi,osc_width,nframes,nconv=self.getDataInfo(sch_file)
        # in helical data collection: each 'cry*sch' makes one dataset
        n_multi=1
        master_file=os.path.join(sch_path,"%s_master.h5"%prefix)

        proc_list=[]
        jpgfile_list=[]

        print "N_MULTI=",n_multi
        for nth_data in range(0,n_multi):
            center_n=int(nframes/2.0)
            start_num_of_this_data=nframes*nth_data+1
            center_of_rotation=start_num_of_this_data+center_n

            conv_startnum=center_of_rotation-int(nconv/2)
            conv_endnum  =center_of_rotation+int(nconv/2)

            filename="%s/%s_%05d-%05d.cbf"%(self.datadir,prefix,conv_startnum,conv_endnum)
            proc_list.append((master_file,conv_startnum,conv_endnum,filename))
            print proc_list

        print "making %5d files"%len(proc_list)
        jpgfile_list.append(easy_mp.pool_map(fixed_func=lambda n: ConvertHD5.ConvertHD5(n).process(), args=proc_list, processes=16))

        print jpgfile_list

if __name__ == "__main__":
    ddd=ResultsZOO(sys.argv[1])
    #ddd.convImages()
    #ddd.procMultiDS()
    sch_files,sch_paths=ddd.getScheudlePaths()

    for sch_file,sch_path in zip(sch_files,sch_paths):
        print "PROCESSING",sch_file
        if sch_file.rfind("multi")!=-1:
            ddd.procMultiDS(sch_file,sch_path)
        elif sch_file.rfind("cry")!=-1:
            ddd.procHelical(sch_file,sch_path)
