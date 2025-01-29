import os,sys,math
sys.path.append("/isilon/BL32XU/BLsoft/PPPP/")
import Subprocess
import random

class ComRefine:
    def __init__(self,proc_path="./"):
        self.pp = os.path.abspath(proc_path)
        self.isHead = False
        self.cellWarning = False
        self.cells_from_command_line = False

    def writeHeader(self):
        """write header of comfile
        2020/09/26
        host_num can be specified between 19-22, when oys has problem (SGE problem?).
        the problem may disappear by rebooting oys01 
        
        2020/09/28
        for SHELX D calculation, nproc (6) and s_vmem (40G) is specified
        """
        
        lines=[]
        #host_num = random.randrange(15,22)
        lines.append("#!/bin/csh\n")
        lines.append("#$ -wd %s\n" % self.pp)
        lines.append("#$ -o %s\n"%self.pp)
        lines.append("#$ -e %s\n"%self.pp)
        #lines.append("#$ -l hostname=oys%02d\n"%host_num)
        #lines.append("#$ -pe par 6\n") # for SHELX D calc (added by HM 2020/09/28)
        #lines.append("#$ -l s_vmem=40G\n") # for SHELX D calc (added by HM 2020/09/28)
        lines.append("setenv OMP_NUM_THREADS 4\n") # for SHELX D calc (added by HM 2020/09/28)
        lines.append("setenv PHENIX_OVERWRITE_ALL true\n")
        self.isHead=True
        return lines

    # 2020/12/09 add by HM
    def writeHeader_slurm(self):
        """ write header of comfile for slurm """
        lines = []
        lines.append("#!/bin/csh\n")
        lines.append("#SBATCH -D %s\n" % self.pp)
        lines.append("#SBATCH -o slurm_o_%J.log\n")
        lines.append("#SBATCH -e slurm_e_%J.log\n")

        lines.append("setenv OMP_NUM_THREADS 4\n")
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

    # 2020/09/21 add by HM
    def reindex_from_xdsascii(self,mtzout,symm,hkl_sort,logfile="reindex.log"):
        #tmplines=self.reindex(mtzin,"reindex.mtz",symm,hkl_sort,logfile="logfile.log",mtzin_abspath=False)
        lines=[]

        # self.pp => 01.MR
        xdsascii_mtz = 'ccp4/XDS_ASCII.mtz'
        mtzin="%s/%s"%(self.pp,xdsascii_mtz)

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
        # modified by HM (2020/09/24)
        lines.append("xray_data.labels=\"IMEAN,SIGIMEAN\"\\\n")
        lines.append("xray_data.low_resolution=25.0 xray_data.high_resolution=%f \\\n"%high_res)
        lines.append("ordered_solvent.mode=every_macro_cycle output.prefix=%s\\\n\n\n"%prefix)
        return lines

    def phenix_refine_fsigf(self,mtzin,pdbin,high_res,prefix="refine",fcol="F",sigf="SIGF"):
        lines=[]
        if self.isHead==False:
            lines+=(self.writeHeader())
        xray_label="\"%s,%s\""%(fcol,sigf)
        mtzin="%s/%s"%(self.pp,mtzin)
        pdbin="%s/%s"%(self.pp,pdbin)
        prefix="%s/%s"%(self.pp,prefix)
        lines.append("phenix.refine %s %s ordered_solvent=true \\\n"%(mtzin,pdbin))
        lines.append("xray_data.low_resolution=25.0 xray_data.high_resolution=%f \\\n"%high_res)
        lines.append("xray_data.labels=%s \\\n"%xray_label)
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
        tmplines=self.jellybody("free.mtz","jelly.mtz",initial_pdb,"jelly.pdb",freer_flags="FreeR_flag")
        comlines+=tmplines
        tmplines=self.phenix_refine("free.mtz","jelly.pdb",resolution_limit,prefix)
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

    # 2020/04/14 modified to add 'reindex' with an argument 'symm'
    def dimple_common_free(self,refmtz,xscale_mtz,symm,resolution_limit,initial_pdb,prefix,outdir="."):
        comlines=[]
        # Reindexing reflection file to the target space group
        tmplines=self.reindex(xscale_mtz,"reindex.mtz",symm,hkl_sort="",logfile="logfile.log")
        comlines+=tmplines
        # Making MTZ file with common Free-R flags with the reference file.
        tmplines=self.common_freerflag(refmtz,"reindex.mtz","free_common.mtz")
        comlines+=tmplines
        # DIMPLE
        tmplines="dimple %s %s %s\n" % ("free_common.mtz", initial_pdb, outdir)
        comlines+=tmplines

        # Writing comfile
        comfile="%s/refine.com"%self.pp
        ofile=open(comfile,"w")
        for line in comlines:
            ofile.write("%s"%line)
        ofile.close()
        os.system("chmod 744 %s"%(comfile))

        return comfile

    # 2020/04/14 modified to add 'reindex' with an argument 'symm'
    def dimpleSimple(self,mtzname,symm,resolution_limit,initial_pdb,prefix,outdir="."):
        comlines=[]
        # Reindexing reflection file to the target space group
        tmplines=self.reindex(mtzname,"reindex.mtz",symm,hkl_sort="",logfile="logfile.log")
        comlines+=tmplines
        # DIMPLE
        tmplines="dimple -f jpeg %s %s %s\n" % ("reindex.mtz", initial_pdb, outdir)
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

    def refine_normal(self,xscale_mtz,symm,resolution_limit,initial_pdb,prefix,hkl_sort="",free_column="FreeR_flag",fcol="F",sigfcol="SIGF"):
        comlines=[]
        tmplines=self.reindex(xscale_mtz,"reindex.mtz",symm,hkl_sort,logfile="logfile.log")
        comlines+=tmplines
        tmplines=self.freer("reindex.mtz","free.mtz")
        comlines+=tmplines
        tmplines=self.jellybody("free.mtz","jelly.mtz",initial_pdb,"jelly.pdb",freer_flags=free_column)
        comlines+=tmplines
        tmplines=self.phenix_refine("free.mtz","jelly.pdb",resolution_limit,prefix)
        fcol="F"
        sigf="SIGF"
        tmplines=self.phenix_refine_fsigf("free.mtz","jelly.pdb",resolution_limit,prefix="refine")
        comlines+=tmplines

        #tmplines=self.jellybody("free.mtz","jelly.mtz",initial_pdb,"jelly.pdb",free_column="FreeR_flag")

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

    
    # 2020/09/21 add by HM
    def simple_refine_from_xdsascii(self,xds_ascii,symm,resolution_limit,initial_pdb,prefix,hkl_sort=""):
        comlines=[]

        #tmplines=self.xds2mtz(xds_ascii,xds_mtz)
        # NOTE: Space group: P43212 (for lysozyme)
        if self.isHead==False:
            comlines+=(self.writeHeader())

        tmplines="xds2mtz.py %s --space-group=P43212\n" % xds_ascii
        comlines+=tmplines
        tmplines=self.reindex_from_xdsascii("reindex.mtz",symm,hkl_sort,logfile="logfile.log")
        comlines+=tmplines
        tmplines=self.freer("reindex.mtz", "free.mtz")
        comlines+=tmplines
        tmplines=self.jellybody("free.mtz","jelly.mtz",initial_pdb,"jelly.pdb",freer_flags="FreeR_flag")
        comlines+=tmplines
        tmplines=self.phenix_refine("free.mtz","jelly.pdb",resolution_limit,prefix)
        comlines+=tmplines

        # Writing comfile
        comfile="%s/refine.com"%self.pp
        ofile=open(comfile,"w")
        for line in comlines:
            ofile.write("%s"%line)
        ofile.close()
        os.system("chmod 744 %s"%(comfile))

        return comfile


    def solve_sad(self, symm, proj_name, phase_dmax, n_try, num_find, anom_atom, solcon, num_dm, nres, hklfile, dmin, seq_file, build_cycle, cell_params):

        shelxd_dmin = dmin + 0.5

        head_lines = self.writeHeader()

        comfile_path = os.path.join(self.pp, "hkl2pdb.com")
        comfile = open(comfile_path, "w")

        for line in head_lines:
            comfile.write("%s" % line)

        comfile.write("shelxc %s << eof > shelxc.log\n" % proj_name)
        comfile.write("SAD %s\n" % hklfile)
        comfile.write("MAXM 20\n")
        comfile.write("FIND %d\n" % num_find)
        comfile.write("SFAC %s\n" % anom_atom)
        comfile.write("NTRY %d\n" % n_try)
        comfile.write("cell %8.3f %8.3f %8.3f %8.3f %8.3f %8.3f\n" % 
            (cell_params[0], cell_params[1], cell_params[2], cell_params[3], cell_params[4], cell_params[5]))
        comfile.write("SPAG %s\n" % symm)
        comfile.write("SHELL %5.2f %5.2f\n" % (phase_dmax, shelxd_dmin))
        comfile.write("eof\n")
        comfile.write("\n")
        comfile.write("shelxd %s_fa > shelxd.log\n" % proj_name)
        comfile.write("\n")
        comfile.write("SHELXE:\n")

        # modified for tsukazaki data analysis (2021/01/16 mat)
        # add -q and -b options

        #comfile.write("shelxe %s %s_fa -s%.2f -m%d -a%d -d%.2f> shelxe_o.log\n" % (proj_name, proj_name, solcon, num_dm, build_cycle, dmin))
        comfile.write("shelxe %s %s_fa -s%.2f -m%d -a%d -q -b -d%.2f> shelxe_o.log\n" % (proj_name, proj_name, solcon, num_dm, build_cycle, dmin))
        #comfile.write("shelxe %s %s_fa -s%.2f -m%d -a%d -i -d%.2f> shelxe_i.log\n" % (proj_name, proj_name, solcon, num_dm, build_cycle, dmin))
        comfile.write("shelxe %s %s_fa -s%.2f -m%d -a%d -q -b -i -d%.2f> shelxe_i.log\n" % (proj_name, proj_name, solcon, num_dm, build_cycle, dmin))

        return comfile_path

    def check_phase(self, symm, proj_name, phase_dmax, n_try, num_find, anom_atom, solcon, num_dm, nres, hklfile, dmin, seq_file, cell_params):

        shelxd_dmin = dmin + 0.5
        head_lines = self.writeHeader()

        comfile_path = os.path.join(self.pp, "checkphase.com")
        comfile = open(comfile_path, "w")

        for line in head_lines:
            comfile.write("%s" % line)

        comfile.write("shelxc %s << eof > shelxc.log\n" % proj_name)
        comfile.write("SAD %s\n" % hklfile)
        comfile.write("MAXM 20\n")
        comfile.write("FIND %d\n" % num_find)
        comfile.write("SFAC %s\n" % anom_atom)
        comfile.write("NTRY %d\n" % n_try)
        comfile.write("cell %8.3f %8.3f %8.3f %8.3f %8.3f %8.3f\n" %
            (cell_params[0], cell_params[1], cell_params[2], cell_params[3], cell_params[4], cell_params[5]))
        comfile.write("SPAG %s\n" % symm)
        comfile.write("SHELL %5.2f %5.2f\n" % (phase_dmax, shelxd_dmin))
        comfile.write("eof\n")
        comfile.write("\n")
        comfile.write("shelxd %s_fa > shelxd.log\n" % proj_name)
        comfile.write("\n")
        comfile.write("SHELXE:\n")
        comfile.write("shelxe %s %s_fa -s%.2f -m%d  -d%.2f> shelxe_o.log\n" % (proj_name, proj_name, solcon, num_dm,  dmin))
        comfile.write("shelxe %s %s_fa -s%.2f -m%d  -i -d%.2f> shelxe_i.log\n" % (proj_name, proj_name, solcon, num_dm,  dmin))

        return comfile_path

    # 2020/12/08 HM (method for ODEN)
    def shelx_sad(self, prefix, hklfile, cell_params, sg, anom_atom, n_anom, n_try, phase_dmax, solv_cnt, n_dm, build_cycle, dmin, batch="sge"):
        """ make comfile for SHELX C/D/E"""

        shelxd_dmin = dmin + 0.5

        comfile = "%s/shelx.com" % self.pp
        #comfile = os.path.join(self.pp, "shelx.com")
        #comfile = open(comfile_path, "w")

        if batch == "sge": 
            head_lines = self.writeHeader()
        elif batch == "slurm": 
            head_lines = self.writeHeader_slurm()

        com_str = head_lines

        # SHELX C
        com_str += "shelxc %s << eof > shelxc.log\n" % prefix
        com_str += "SAD %s\n" % hklfile
        #com_str += "CELL %8.3f %8.3f %8.3f %8.3f %8.3f %8.3f\n" % (cell_params[0], cell_params[1], cell_params[2], cell_params[3], cell_params[4], cell_params[5])
        com_str += "CELL %s\n" % (cell_params)
        com_str += "SPAG %s\n" % sg 
        com_str += "SFAC %s\n" % anom_atom
        com_str += "MAXM 20\n" # reverse memory in units of 1M reflections
        com_str += "FIND %d\n" % n_anom
        com_str += "NTRY %d\n" % n_try
        com_str += "SHELL %5.2f %5.2f\n" % (phase_dmax, shelxd_dmin)
        com_str += "eof\n"
        com_str += "\n"

        # SHELX D
        com_str += "shelxd %s_fa > shelxd.log\n" % prefix
        com_str += "\n"

        # SHELX E
        # modified (2021/01/16 mat)
        # add -q and -b options for tsukazaki data anaylsis
        com_str += "shelxe %s %s_fa -s%.2f -m%d -a%d -q -b -d%.2f > shelxe_o.log\n" % (prefix, prefix, solv_cnt, n_dm, build_cycle, dmin)
        com_str += "shelxe %s %s_fa -s%.2f -m%d -a%d -q -b -i -d%.2f > shelxe_i.log\n" % (prefix, prefix, solv_cnt, n_dm, build_cycle, dmin)

        with open(comfile, "w") as fo:
            for line in com_str:
                fo.write(line)

        return comfile

    # 2021/01/16 HM (method for ODEN)
    def shelx_siras(self, prefix, hklfile_ano, hklfile_nat, cell_params, sg, anom_atom, n_anom, n_try, phase_dmax, solv_cnt, n_dm, build_cycle, dmin, batch="sge"):
        """ make comfile for SIRAS using SHELX C/D/E"""

        shelxd_dmin = dmin + 0.5

        comfile = "%s/shelx.com" % self.pp
        #comfile = os.path.join(self.pp, "shelx.com")
        #comfile = open(comfile_path, "w")

        if batch == "sge": 
            head_lines = self.writeHeader()
        elif batch == "slurm": 
            head_lines = self.writeHeader_slurm()

        com_str = head_lines

        # SHELX C
        com_str += "shelxc %s << eof > shelxc.log\n" % prefix
        com_str += "SIRA %s\n" % hklfile_ano
        com_str += "NAT %s\n" % hklfile_nat
        #com_str += "CELL %8.3f %8.3f %8.3f %8.3f %8.3f %8.3f\n" % (cell_params[0], cell_params[1], cell_params[2], cell_params[3], cell_params[4], cell_params[5])
        com_str += "CELL %s\n" % (cell_params)
        com_str += "SPAG %s\n" % sg 
        com_str += "SFAC %s\n" % anom_atom
        com_str += "MAXM 20\n" # reverse memory in units of 1M reflections
        com_str += "FIND %d\n" % n_anom
        com_str += "NTRY %d\n" % n_try
        com_str += "SHELL %5.2f %5.2f\n" % (phase_dmax, shelxd_dmin)
        com_str += "eof\n"
        com_str += "\n"

        # SHELX D
        com_str += "shelxd %s_fa > shelxd.log\n" % prefix
        com_str += "\n"

        # SHELX E
        # for SIRAS (previously used parameters)
        #com_str += "shelxe %s %s_fa -m100 -s0.55 -l2 -d0.1 -e2.7 -b -a5 -i > shelxe_i.log\n" % (prefix, prefix)
        # -e default: dmin + 0.2

        #com_str += "shelxe %s %s_fa -m%d -s%.2f -l2 -d%.2f -b -a%d > shelxe_o.log\n" % (prefix, prefix, n_dm, solv_cnt, dmin, build_cycle )
        #com_str += "shelxe %s %s_fa -m%d -s%.2f -l2 -d%.2f -b -a%d -i > shelxe_i.log\n" % (prefix, prefix, n_dm, solv_cnt, dmin, build_cycle )
        # further add -q option
        com_str += "shelxe %s %s_fa -m%d -s%.2f -l2 -d%.2f -b -a%d -q > shelxe_o.log\n" % (prefix, prefix, n_dm, solv_cnt, dmin, build_cycle )
        com_str += "shelxe %s %s_fa -m%d -s%.2f -l2 -d%.2f -b -a%d -q -i > shelxe_i.log\n" % (prefix, prefix, n_dm, solv_cnt, dmin, build_cycle )
        with open(comfile, "w") as fo:
            for line in com_str:
                fo.write(line)

        return comfile


    # add by HM (2020/09/26)
    # original comfile written by KH
    # phs file: only file name (lys.phs or lys_i.phs)
    # TODO: check
    def phs2map_cc(self, prefix, cell_params, symm, base_model, phs):
        """write mapcc.com (including phs2mtz)
        first phs2mtz will convert .phs to .mtz,
        then phenix.map_cc_mtz_pdb will run
        """
        head_lines = self.writeHeader()

        comfile_path = os.path.join(self.pp, 'phs2mapcc.com')
        comfile = open(comfile_path, 'w')

        for line in head_lines:
            comfile.write('%s' % line)

        # write comfile to make .phs -> .mtz file using f2mtz
        comfile.write('set PREFIX=%s\n' % prefix)
        comfile.write('set CELL=%s\n' % cell_params)
        comfile.write('set SYMM=%s\n' % symm)
        comfile.write('set MODEL=%s\n' % base_model)

        comfile.write('f2mtz hklin ../00.SAD/%s hklout $PREFIX.mtz > f2mtz.log << END\n' % (phs))
        comfile.write('cell $CELL\n')
        comfile.write('symmetry $SYMM\n')
        comfile.write('labout H K L FP FOM PHIB SIGFP\n')
        comfile.write('CTYPOUT H H H F W P Q\n')
        comfile.wirte('END\n')
        
        # phenix.get_cc_mtz_pdb
        comfile.write('phenix.get_cc_mtz_pdb ./lys_phase.mtz $MODEL > mapcc.log\n')
       
        # grep correlation info 
        comfile.write('grep "Correlation in region of model" mapcc.log > mapcc.dat\n')
        comfile.write('grep "overall CC" mapcc.log >> mapcc.dat\n')
        comfile.write('grep "local CC" mapcc.log >> mapcc.dat\n') 

        return comfile_path

    # 2020/09/29 (add by HM)
    def map_cc(self, mtz, base_model):
        """write mapcc.com
        write mapcc.com to run phenix.map_cc_mtz_pdb (only)
        """
        head_lines = self.writeHeader()

        comfile_path = os.path.join(self.pp, 'mapcc.com')
        comfile = open(comfile_path, 'w')

        for line in head_lines:
            comfile.write('%s' % line)

        # phenix.get_cc_mtz_pdb
        comfile.write("set MTZ='%s'\n" % (mtz))
        comfile.write("set MODEL='%s'\n" % (base_model))
        comfile.write('phenix.get_cc_mtz_pdb $MTZ $MODEL > mapcc.log\n')
       
        # grep correlation info 
        comfile.write('grep "Correlation in region of model" mapcc.log > mapcc.dat\n')
        comfile.write('grep "overall CC" mapcc.log >> mapcc.dat\n')
        comfile.write('grep "local CC" mapcc.log >> mapcc.dat\n') 

        return comfile_path

    # add by HM (2020/09/26)
    # original comfile written by KH
    # TODO: check
    def lys_wilson(self,mtz):
        """wirte wilson.com
        default resolution range 4.0 - 2.0 A
        number of residue: 119 (default)
        """
        head_lines = self.writeHeader()

        comfile_path = os.path.join(self.pp, 'wilson.com')
        comfile = open(comfile_path, 'w')

        for line in head_lines:
            comfile.write('%s' % line)

        # wilson
        comfile.write("set MTZ='%s'\n" % mtz)
        comfile.write('wilson hklin $MTZ << EOF-wil > wilson.log\n')
        comfile.write('rscale 4.0 2.0\n')
        comfile.write('wilson observed\n')
        comfile.write('nresidues 119\n')
        comfile.write('LABIN FP=F SIGFP=SIGF\n')
        comfile.write('EOF-wil\n')

        comfile.write('grep "Least squares straight" wilson.log > isob.dat\n')

        return comfile_path

    # add by HM (2020/11/10)
    def wilson(self, mtz, nres):
        """ wirte 'wilson.com'
        default resolution range 4.0 - 2.0 A
        Params:
            mtz (str): mtz file
            nres (int): number of residues
        Returns:
            comfile: com file for calculate wilson B
        """
        head_lines = self.writeHeader()

        comfile_path = os.path.join(self.pp, 'wilson.com')
        comfile = open(comfile_path, 'w')

        for line in head_lines:
            comfile.write('%s' % line)

        # wilson
        comfile.write("set MTZ='%s'\n" % mtz)
        comfile.write('wilson hklin $MTZ << EOF-wil > wilson.log\n')
        comfile.write('rscale 4.0 2.0\n')
        comfile.write('wilson observed\n')
        comfile.write('nresidues %s\n' % (nres))
        comfile.write('LABIN FP=F SIGFP=SIGF\n')
        comfile.write('EOF-wil\n')

        comfile.write('grep "Least squares straight" wilson.log > isob.dat\n')

        return comfile_path


    # 2020/09/29 (add by HM)
    def anode(self, prefix):
        """execute ANODE"""
        head_lines = self.writeHeader()
        
        comfile_path = os.path.join(self.pp, 'anode.com')
        comfile = open(comfile_path, 'w')

        for line in head_lines:
            comfile.write('%s' % line)

        # ANODE
        comfile.write('anode %s > anode.log\n' % (prefix)) 
        

        return comfile_path

    def phs2mtz(self, prefix, cell_params):
        """convert .phs -> .mtz
        This method has critical error. Use phs2mtz_mod.
        """
        head_lines = self.writeHeader()

        comfile_path = os.path.join(self.pp, 'phs2mtz.com')
        comfile = open(comfile_path, 'w')

        for line in head_lines:
            comfile.write('%s' % line)


        # phs2mtz
        comfile.write("set PREFIX='%s'\n" %(prefix))
        comfile.write("set CELL='%s'\n" % (cell_params))
        comfile.write("set SYMM='P43212'\n")
        
        comfile.write("f2mtz hklin $PREFIX.phs hklout $PREFIX.mtz > f2mtz.log << END\n")
        comfile.write("cell $CELL\n")
        comfile.write("symmetry $SYMM\n")
        comfile.write("labout H K L FP FOM PHIB SIGFP\n")
        comfile.write("CTYPOUT H H H F W P Q\n")
        comfile.write("END\n")

        return comfile_path 

    def phs2mtz_mod(self, ans_phs_prefix, symm, cell_params):
        """convert .phs -> .mtz
        ans_phs is the answer .phs file from SHELX
        previous phs2mtz function has critical error
        (choose only original .phs file even when the answer is inverse)
        """
        head_lines = self.writeHeader()

        comfile_path = os.path.join(self.pp, 'phs2mtz.com')
        comfile = open(comfile_path, 'w')

        for line in head_lines:
            comfile.write('%s' % line)


        # phs2mtz
        #comfile.write("set PREFIX='%s'\n" %(prefix))
        comfile.write("set ANS='%s'\n" %(ans_phs_prefix))
        comfile.write("set CELL='%s'\n" % (cell_params))
        comfile.write("set SYMM='%s'\n" % symm)
        
        comfile.write("f2mtz hklin $ANS.phs hklout $ANS.mtz > f2mtz.log << END\n")
        comfile.write("cell $CELL\n")
        comfile.write("symmetry $SYMM\n")
        comfile.write("labout H K L FP FOM PHIB SIGFP\n")
        comfile.write("CTYPOUT H H H F W P Q\n")
        comfile.write("END\n")

        return comfile_path 

    def phenix_merging_statistics(self, hkl):
        """ Run phenix.merging_statistics"""
        head_lines = self.writeHeader()

        comfile_path = os.path.join(self.pp, 'pms.com')
        comfile = open(comfile_path, 'w')

        for line in head_lines:
            comfile.write('%s' % line)


        # phs2mtz
        comfile.write("set HKL='%s'\n" %(hkl))
        comfile.write("phenix.merging_statistics $HKL > merging_stats.log\n")

        return comfile_path


if __name__ == "__main__":
    comf=ComRefine()
    #comf.simple_refine("/isilon/com","xscale.mtz","P212121",1.8,"/isilon/model.pdb","refine")
    #comf.simple_refine("/isilon/com","xscale.mtz","P212121",1.8,"/isilon/model.pdb","refine")

    #def solve_sad(self, symm, proj_name, phase_dmax, n_try, num_find, anom_atom, solcon, num_dm, nres, hklfile, dmin, seq_file, build_cycle, cell_params):
    #comf.solve_sad("P43212", "lys", 25,  10, 12, "S", 0.40, 50, 118, "xscale.hkl", 1.3, "lys.pir", 5, [78,78,36,90,90,90])

    comf.dimple_common_free("foo/reference.mtz","ccp4/xscale.mtz","C2",3.5,"foo/model.pdb","toma")
