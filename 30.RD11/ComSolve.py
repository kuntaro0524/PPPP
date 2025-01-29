import os,sys,math
sys.path.append("/isilon/BL32XU/BLsoft/PPPP/")
import Subprocess

class ComRefine:
    def __init__(self,proc_path="./"):
        self.pp = os.path.abspath(proc_path)
        self.isHead = False
        self.cellWarning = False
        self.cells_from_command_line = False

    def writeHeader(self):
        lines=[]
        lines.append("#!/bin/csh\n")
        lines.append("#$ -cwd\n")
        lines.append("#$ -o %s\n"%self.pp)
        lines.append("#$ -e %s\n"%self.pp)
        lines.append("setenv PHENIX_OVERWRITE_ALL true\n")
        self.isHead=True
        return lines

    def reindex(self,mtzin,mtzout,symm,hkl_sort,logfile="reindex.log",mtzin_abspath=False):
        #tmplines=self.reindex(mtzin,"reindex.mtz",symm,hkl_sort,logfile="logfile.log",mtzin_abspath=False)
        lines=[]
        if mtzin_abspath == False:
            mtzin="%s/%s"%(self.pp,mtzin)
        else:
            mtzin=mtzin
        mtzout="%s/%s"%(self.pp,mtzout)
        logfile="%s/%s"%(self.pp,logfile)

        if self.isHead==False:
            lines+=(self.writeHeader())
        lines.append("reindex hklin %s hklout %s <<EOF > %s\n"%(mtzin,mtzout,logfile))
        if hkl_sort!="":
            lines.append("reindex HKL %s\n"%hkl_sort)

        lines.append("symm %s\n"%symm)
        lines.append("end\n")
        lines.append("EOF\n\n")

        return lines

    def extractFreeR(self,mtzin):
        sp=Subprocess.Subprocess()
        com="mtzdmp %s"%mtzin
        #sp.proc_180626(com)
        rc,st,err=sp.proc_communicate(com)
    
        for i in st.split("\n"):
            if i.rfind("Free")!=-1 or i.rfind("free")!=-1:
                if i.rfind(" I ")!=-1:
                    cols=i.split()
                    for col in cols:
                        if col.rfind("free")!=-1 or col.rfind("Free")!=-1:
                            return col
        return "none"

    def freer(self,mtzin,mtzout):
        lines=[]
        if self.isHead==False:
            lines+=(self.writeHeader())
        mtzin="%s/%s"%(self.pp,mtzin)
        mtzout="%s/%s"%(self.pp,mtzout)
        logfile="%s/free.log"%(self.pp)
        lines.append("uniqueify -p 0.05 %s %s > %s\n\n"%(mtzin,mtzout,logfile))
        return lines

    def jellybody(self,mtzin,mtzout,pdbin,pdbout,logfile="jelly.log",fp_col="F",sigfp_col="SIGF",freer_flags="R-free-flags",n_cycle=50):
        mtzin="%s/%s"%(self.pp,mtzin)
        mtzout="%s/%s"%(self.pp,mtzout)
        pdbout="%s/%s"%(self.pp,pdbout)
        logfile="%s/%s"%(self.pp,logfile)
        lines=[]
        if self.isHead==False:
            lines+=(self.writeHeader())
        lines.append("refmac5 \\\n")
        lines.append("hklin %s \\\n"%mtzin)
        lines.append("hklout %s \\\n"%mtzout)
        lines.append("xyzin %s \\\n"%pdbin)
        lines.append("xyzout %s << eof > %s \n"%(pdbout,logfile))
        lines.append("refi     type REST     resi MLKF     meth CGMAT     bref ISOT \n")
        lines.append("ncyc %d\n"%n_cycle)
        lines.append("scal     type SIMP     LSSC     ANISO     EXPE\n")
        lines.append("solvent YES\n")
        lines.append("weight     AUTO\n")
        lines.append("LABIN FP=%s SIGFP=%s FREE=%s\n"%(fp_col,sigfp_col,freer_flags))
        lines.append("RIDG DIST SIGM 0.02\n")
        lines.append("END\n")
        lines.append("eof\n\n")

        return lines

    def phenix_refine_lowreso(self,mtzin,pdbin,high_res,prefix="refine",pdbin_abspath=False,mtzin_abspath=False,free_column="R-free-flags"):
        lines=[]
        if self.isHead==False:
            lines+=(self.writeHeader())
        if mtzin_abspath==True:
            mtzin=mtzin
        else:
            mtzin="%s/%s"%(self.pp,mtzin)
        if pdbin_abspath==False:
            pdbin="%s/%s"%(self.pp,pdbin)
        else:
            pdbin=pdbin
        prefix="%s/%s"%(self.pp,prefix)
        lines.append("phenix.refine %s %s strategy=individual_sites+individual_adp+tls+occupancies nqh_flip=false \
            output.prefix=%s  optimize_xyz_weight=true optimize_adp_weight=true proc=1 \n\n"%(mtzin,pdbin,prefix))
        return lines

    def phenix_refine_with_efffile(self,mtzin,eff_file,resolution_limit,prefix="refine",):
        lines=[]
        if self.isHead==False:
            lines+=(self.writeHeader())
        mtzin="%s/%s"%(self.pp,mtzin)
        prefix="%s/%s"%(self.pp,prefix)
        lines.append("setenv PHENIX_OVERWRITE_ALL true; phenix.refine --unused_ok %s %s nqh_flip=false \
            xray_data.labels=\"IMEAN,SIGIMEAN\" \
            output.prefix=%s proc=1 \n\n"%(mtzin,eff_file,prefix))
        return lines

    def phenix_refine_with_all_from_efffile(self,mtzin,eff_file,prefix="refine"):
        lines=[]
        if self.isHead==False:
            lines+=(self.writeHeader())
        mtzin="%s/%s"%(self.pp,mtzin)
        prefix="%s/%s"%(self.pp,prefix)
        lines.append("sleep 10.0\n")
        lines.append("setenv PHENIX_OVERWRITE_ALL true; phenix.refine --unused_ok %s %s nqh_flip=false \
            xray_data.labels=\"IMEAN,SIGIMEAN\" \
            proc=1 output.prefix=%s \n\n"%(mtzin,eff_file,prefix))
        return lines

    def phenix_refine_with_efffile_except_for_resol(self,mtzin,eff_file,dmin,prefix="refine"):
        lines=[]
        if self.isHead==False:
            lines+=(self.writeHeader())

        mtzin="%s/%s"%(self.pp,mtzin)
        prefix="%s/%s"%(self.pp,prefix)

        # Uncheck discrepancy between 'comman line unit cells' and 'unit cells in PDB/MTZ files'
        h1 = ""
        h2 = ""
        if self.cellWarning == True:
            h1 = "refinement.input.symmetry_safety_check=warning "
        # Cell parameters from command line
        if self.cells_from_command_line == True:
            h2 = "--unit_cell='%s' --space_group=%s" % (self.cells,self.spg)
        lines.append("sleep 10.0\n")
        lines.append("setenv PHENIX_OVERWRITE_ALL true; phenix.refine --unused_ok %s %s nqh_flip=false \
            xray_data.labels=\"IMEAN,SIGIMEAN\" \
            proc=1 output.prefix=%s xray_data.high_resolution=%s %s %s\n\n"%(mtzin,eff_file,prefix,dmin,h1,h2))
        return lines

    def phenix_refine(self,mtzin,pdbin,high_res,prefix="refine"):
        lines=[]
        if self.isHead==False:
            lines+=(self.writeHeader())
        mtzin="%s/%s"%(self.pp,mtzin)
        pdbin="%s/%s"%(self.pp,pdbin)
        prefix="%s/%s"%(self.pp,prefix)
        lines.append("phenix.refine %s %s ordered_solvent=true \\\n"%(mtzin,pdbin))
        lines.append("xray_data.low_resolution=25.0 xray_data.high_resolution=%f \\\n"%high_res)
        lines.append("ordered_solvent.mode=every_macro_cycle output.prefix=%s\\\n\n\n"%prefix)
        return lines

    # refmtz : should be given as "Absolute path"
    def common_freerflag(self,refmtz,mtzin,mtzout):
        lines=[]
        if self.isHead==False:
            lines+=(self.writeHeader())
        mtzin="%s/%s"%(self.pp,mtzin)
        mtzout="%s/%s"%(self.pp,mtzout)
        # copy_free_R_flag.py -r ../../../../../AT2R_4A03Fab_refine_140.mtz ./xscale.mtz -o free.mtz
        lines.append("copy_free_R_flag.py -r %s %s -o %s\n\n"%(refmtz,mtzin,mtzout))
        return lines

    def do_molrep(self,mtzin,modelin,nmon,fcol,sigfcol):
        mtzin="%s/%s"%(self.pp,mtzin)
        logfile="%s/%s"%(self.pp,"molrep.log")

        lines=[]
        lines.append("molrep HKLIN %s \\\n"%mtzin)
        lines.append("MODEL %s \\\n"%modelin)
        lines.append("PATH_OUT %s/ << stop > %s\n"%(self.pp,logfile))
        lines.append("DOC  Y \n")
        lines.append("LABIN F=%s  SIGF=%s \n"%(fcol,sigfcol))
        lines.append("NMON   %s \n"%nmon)
        lines.append("NP     3 \n")
        lines.append("NPT    10 \n")
        lines.append("_END \n")
        lines.append("stop\n\n")
        return lines

    # initial_pdb : should be given as "Absolute path"
    def simple_refine(self,xscale_mtz,symm,resolution_limit,initial_pdb,prefix,hkl_sort=""):
        comlines=[]
        tmplines=self.reindex(xscale_mtz,"reindex.mtz",symm,hkl_sort,logfile="logfile.log")
        comlines+=tmplines
        tmplines=self.freer("reindex.mtz","free.mtz")
        comlines+=tmplines
        tmplines=self.jellybody("free.mtz","jelly.mtz",initial_pdb,"jelly.pdb")
        comlines+=tmplines
        tmplines=self.phenix_refine("free.mtz","jelly.pdb",resolution_limit,prefix)
        comlines+=tmplines
        return comlines

    # refmtz : should be given as "Absolute path"
    def refine_common_free(self,refmtz,xscale_mtz,symm,resolution_limit,initial_pdb,prefix,hkl_sort="",free_column="R-free-flags"):
        comlines=[]
        tmplines=self.reindex(xscale_mtz,"reindex.mtz",symm,hkl_sort,logfile="logfile.log")
        comlines+=tmplines
        tmplines=self.common_freerflag(refmtz,"reindex.mtz","free_common.mtz")
        comlines+=tmplines
        tmplines=self.jellybody("free_common.mtz","jelly.mtz",initial_pdb,"jelly.pdb",freer_flags=free_column)
        comlines+=tmplines
        tmplines=self.phenix_refine("free_common.mtz","jelly.pdb",resolution_limit,prefix)
        comlines+=tmplines

        # Writing comfile
        comfile="%s/refine.com"%self.pp
        ofile=open(comfile,"w")
        for line in comlines:
            ofile.write("%s"%line)
        ofile.close()
        os.system("chmod 744 %s"%(comfile))

        return comfile

    def rerun_XDS(self,path,dmin,anomalous="yes"):
        comlines=[]
        tmplines=self.reindex(xscale_mtz,"reindex.mtz",symm,hkl_sort,logfile="logfile.log")
        comlines+=tmplines
        tmplines=self.common_freerflag(refmtz,"reindex.mtz","free_common.mtz")
        comlines+=tmplines
        tmplines=self.do_molrep("free_common.mtz",initial_pdb,nmon,fcol,sigfcol)
        comlines+=tmplines
        mr_pdb="%s/molrep.pdb"%(self.pp)
        tmplines=self.jellybody("free_common.mtz","jelly.mtz",mr_pdb,"jelly.pdb",freer_flags=free_column)
        comlines+=tmplines

    # refmtz : should be given as "Absolute path"
    def mr_refine_common_free(self,refmtz,xscale_mtz,symm,resolution_limit,initial_pdb,prefix,hkl_sort="",free_column="R-free-flags",nmon=1,fcol="F",sigfcol="SIGF"):
        comlines=[]
        tmplines=self.reindex(xscale_mtz,"reindex.mtz",symm,hkl_sort,logfile="logfile.log")
        comlines+=tmplines
        tmplines=self.common_freerflag(refmtz,"reindex.mtz","free_common.mtz")
        comlines+=tmplines
        tmplines=self.do_molrep("free_common.mtz",initial_pdb,nmon,fcol,sigfcol)
        comlines+=tmplines
        mr_pdb="%s/molrep.pdb"%(self.pp)
        tmplines=self.jellybody("free_common.mtz","jelly.mtz",mr_pdb,"jelly.pdb",freer_flags=free_column)
        comlines+=tmplines
        tmplines=self.phenix_refine("free_common.mtz","jelly.pdb",resolution_limit,prefix)
        comlines+=tmplines

        # Writing comfile
        comfile="%s/refine.com"%self.pp
        ofile=open(comfile,"w")
        for line in comlines:
            ofile.write("%s"%line)
        ofile.close()
        os.system("chmod 744 %s"%(comfile))

        return comfile

    def refine_compare_cluster_lowreso(self,refmtz,xscale_mtz,symm,resolution_limit,initial_pdb,prefix,hkl_sort=""):
        comlines=[]
        tmplines=self.reindex(xscale_mtz,"reindex.mtz",symm,hkl_sort,logfile="logfile.log")
        comlines+=tmplines
        tmplines=self.common_freerflag(refmtz,"reindex.mtz","free_common.mtz")
        comlines+=tmplines
        tmplines=self.phenix_refine_lowreso("free_common.mtz",initial_pdb,resolution_limit,prefix,pdbin_abspath=True)
        comlines+=tmplines

        # Writing comfile
        comfile="%s/refine.com"%self.pp
        ofile=open(comfile,"w")
        for line in comlines:
            ofile.write("%s"%line)
        ofile.close()
        os.system("chmod 744 %s"%(comfile))

        return comfile

    # KOHDA
    def ridx_freer_phx_eff(self,refmtz,mtzin,symm,resolution_limit,eff_file,hkl_sort="",mtzin_abspath=False):
        comlines=[]
        tmplines=self.reindex(mtzin,"reindex.mtz",symm,hkl_sort,logfile="logfile.log",mtzin_abspath=mtzin_abspath)
        comlines+=tmplines
        tmplines=self.common_freerflag(refmtz,"reindex.mtz","free_common.mtz")
        comlines+=tmplines
        tmplines=self.phenix_refine_with_efffile_except_for_resol("free_common.mtz",eff_file,resolution_limit)
        comlines+=tmplines

        # Writing comfile
        comfile="%s/refine.com"%self.pp
        ofile=open(comfile,"w")
        for line in comlines:
            ofile.write("%s"%line)
        ofile.close()
        os.system("chmod 744 %s"%(comfile))

        return comfile

    # refmtz : should be given as "Absolute path"
    def ridx_freer_phx_low(self,refmtz,xscale_mtz,symm,resolution_limit,initial_pdb,prefix,hkl_sort=""):
        comlines=[]
        tmplines=self.reindex(xscale_mtz,"reindex.mtz",symm,hkl_sort,logfile="logfile.log")
        comlines+=tmplines
        tmplines=self.common_freerflag(refmtz,"reindex.mtz","free_common.mtz")
        comlines+=tmplines
        comlines+="sleep 20.0\n"
        tmplines=self.phenix_refine_lowreso("free_common.mtz",initial_pdb,resolution_limit,prefix,pdbin_abspath=True,mtzin_abspath=False)
        comlines+=tmplines

        # Writing comfile
        comfile="%s/refine.com"%self.pp
        ofile=open(comfile,"w")
        for line in comlines:
            ofile.write("%s"%line)
        ofile.close()
        os.system("chmod 744 %s"%(comfile))

        return comfile

    def setThroughCellDiff(self):
        self.cellWarning = True

    def setCellParams(self, cells, spg):
        self.cells_from_command_line = True
        self.cells = cells
        self.spg = spg

    # refine only
    def refine_only(self,mtzin,pdbin,resolution_limit,prefix,pdbin_abspath=True,mtzin_abspath=True):
        comlines=[]

        #def phenix_refine_lowreso(self,mtzin,pdbin,high_res,prefix="refine",pdbin_abspath=False,mtzin_abspath=False,free_column="R-free-flags"):
        tmplines=self.phenix_refine_lowreso(mtzin,pdbin,resolution_limit,prefix,pdbin_abspath=pdbin_abspath,mtzin_abspath=mtzin_abspath)
        comlines+=tmplines

        # Writing comfile
        comfile="%s/refine_only.com"%self.pp
        ofile=open(comfile,"w")
        for line in comlines:
            ofile.write("%s"%line)
        ofile.close()
        os.system("chmod 744 %s"%(comfile))

        return comfile

    # refmtz : should be given as "Absolute path"
    def refine_phenix_low_only(self,refmtz,xscale_mtz,symm,resolution_limit,initial_pdb,prefix,hkl_sort="",free_column="R-free-flags"):
        comlines=[]

        tmplines=self.phenix_refine_lowreso("free_common.mtz","jelly.pdb",resolution_limit,prefix)

        comlines+=tmplines

        # Writing comfile
        comfile="%s/refine_low.com"%self.pp
        ofile=open(comfile,"w")
        for line in comlines:
            ofile.write("%s"%line)
        ofile.close()
        os.system("chmod 744 %s"%(comfile))

        return comfile

    # phenix.refine with .eff template file 2018/10/25 coded 
    def refine_with_efffile(self,refmtz,xscale_mtz,symm,resolution_limit,eff_file,prefix):
        comlines=[]
        tmplines=self.common_freerflag(refmtz,xscale_mtz,"free_common.mtz")
        comlines+=tmplines
        tmplines=self.phenix_refine_with_efffile("free_common.mtz",eff_file,resolution_limit,prefix)
        comlines+=tmplines

        # Writing comfile
        comfile="%s/refine.com"%self.pp
        ofile=open(comfile,"w")
        for line in comlines:
            ofile.write("%s"%line)
        ofile.close()
        os.system("chmod 744 %s"%(comfile))

        return comfile

    # from XDS_ASCII.HKL -> MTZ -> common freer flags -> Rigid body refinement
    # restrained refinement -> Keitaro's refinement
    def refine_from_xdsascii(self,refmtz,xds_ascii,symm,resolution_limit,initial_pdb,prefix,hkl_sort=""):
        comlines=[]

        tmplines=self.xds2mtz(xds_ascii,xds_mtz)
        tmplines=self.reindex(xscale_mtz,"reindex.mtz",symm,hkl_sort,logfile="logfile.log")
        comlines+=tmplines
        tmplines=self.common_freerflag(refmtz,"reindex.mtz","free_common.mtz")
        comlines+=tmplines
        tmplines=self.jellybody("free_common.mtz","jelly.mtz",initial_pdb,"jelly.pdb",freer_flags="R-free-flags")
        comlines+=tmplines
        tmplines=self.phenix_refine("free_common.mtz","jelly.pdb",resolution_limit,prefix)
        comlines+=tmplines

        # Writing comfile
        comfile="%s/refine.com"%self.pp
        ofile=open(comfile,"w")
        for line in comlines:
            ofile.write("%s"%line)
        ofile.close()
        os.system("chmod 744 %s"%(comfile))

        return comfile

    def solve_sad(self):

if __name__ == "__main__":
    comf=ComRefine()
    #comf.simple_refine("/isilon/com","xscale.mtz","P212121",1.8,"/isilon/model.pdb","refine")
    #comf.simple_refine("/isilon/com","xscale.mtz","P212121",1.8,"/isilon/model.pdb","refine")

"""
	comlines=[]
	
	tmplines=comf.reindex("./xscale.mtz","reindex.mtz","P212121",logfile="logfile.log")
	comlines+=tmplines
	
	tmplines=(comf.freer("reindex.mtz","free.mtz"))
	comlines+=tmplines
	
	tmplines=comf.jellybody("free.mtz","jelly.mtz","model.pdb","jelly.pdb")
	comlines+=tmplines
	
	tmplines=comf.phenix_refine("free.mtz","jelly.pdb",2.5)
	comlines+=tmplines
	
	for line in comlines:
		print line,
"""
