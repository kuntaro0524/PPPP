import sys,os
sys.path.append("/isilon/BL32XU/BLsoft/PPPP/")
sys.path.append("/isilon/BL32XU/BLsoft/PPPP/11.ClusterAnalysis/")
sys.path.append("/isilon/BL32XU/BLsoft/PPPP/18.Report/")

import glob,numpy
import DirectoryProc
import MyDate
import time
import XSCALEReporter
import AnalyzeDirInKAMO
import MultiMergeLogKAMO

# DEBUG flag
isDebug = True
isIncludeMTZ = False

class Unko():

    def __init__(self, root_dir):
        self.root_dir = root_dir
        #print "RRRRRRRRRRRRRRRR=",root_dir
        self.isPrep = False
        self.required_files = ["CORRECT.LP", "XDS_ASCII.HKL"]
        
        self.isMTZ = False

    def addRequiredFile(self, filename):
        self.required_files.append(filename)

    def prep(self):
        adka = AnalyzeDirInKAMO.AnalyzeDirInKAMO(self.root_dir)
        #print "Unko.prep: ROOT_DIR = %s" % self.root_dir

        # large wedge paths
        self.success_paths = adka.getGoodLargeWedgeDirs()
        
        # merge directories
        self.merge_dirs = adka.getMergeDirs()

        self.isPrep = True

    def makeReportLargeWedge(self, option = "None"):
        if self.isPrep == False:
            self.prep()
        arc_large = []

        if self.isMTZ == True:
            print self.isMTZ

        for ok in self.success_paths:
            print ok
            for required_file in self.required_files:
                file_path = os.path.join(ok, required_file)
                if os.path.exists(file_path) == True:
                    rel_path = os.path.relpath(file_path, "./")
                    arc_large.append(rel_path)
                    if rel_path.rfind("XDS_ASCII.HKL")!=-1:
                        ana_dir = os.path.relpath(file_path)
                        print ana_dir
                        command = "cd %s\n xds2mtz.py\n cd %s \n " % (ana_dir, self.root_dir)
                        os.system(command)

        return arc_large

    def makeArchiveLargeWedge(self):
        #print "DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD"
        if self.isPrep == False:
            self.prep()

        arc_large = []

        if self.isMTZ == True:
            print self.isMTZ

        #print "TESTETESTESTST",self.success_paths

        for ok in self.success_paths:
            #print "OKAY=",ok
            for required_file in self.required_files:
                file_path = os.path.join(ok, required_file)
                if os.path.exists(file_path) == True:
                    rel_path = os.path.relpath(file_path, "./")
                    arc_large.append(rel_path)

        return arc_large

    def getListOfGoodMergeDirs(self):
        if self.isPrep == False:
            self.prep()

        # Check paths as 'absolute' paths
        merge_paths = []
        for merge_dir in self.merge_dirs:
            joined_path = os.path.join(self.root_dir, merge_dir)
            abs_path = os.path.abspath(joined_path)
            merge_paths.append(abs_path)

        # For 'merge' directories
        final_paths = []
        for check_path in merge_paths:
            #print "Checking [merging directory]=%s" % check_path
            # Finding 'final' directories in designated paths
            dp=DirectoryProc.DirectoryProc(check_path)
            first_layers = dp.findDirs()

            # Paths with 'final'
            for directory in first_layers:
                #print "directory=",directory
                if directory.rfind("final") != -1:
                    connected_path = os.path.join(check_path, directory)
                    abs_path = os.path.abspath(connected_path)
                    print "Appending %s" % abs_path
                    final_paths.append(abs_path)
                else:
                    continue

        # Okay paths
        okay_paths = []
        for final_dir in final_paths:
            kamo_merge_log = "%s/multi_merge.log" % final_dir
            if os.path.exists(kamo_merge_log) == True:
                MMLK = MultiMergeLogKAMO.MultiMergeLogKAMO(kamo_merge_log)
                status = MMLK.checkStatus()
                isDone = MMLK.isDone()
                if status == 0 and isDone == True:
                    okay_paths.append(final_dir)

        #print okay_paths
        return  okay_paths

    # Input information: 'okay_dirs' : merge_*/*_final/
    # okay_dir: "each merge directory" with 'final scaling'
    def findFinalResultsDir(self, okay_dirs):
        # Find a cluster with the maximum number of datasets
        max_cluster_dirs = []
        for okay_dir in okay_dirs:
            # Directory
            dp=DirectoryProc.DirectoryProc(okay_dir)
            first_layers = dp.findDirs()
       
            #print "Processing: %s" % okay_dir
            max_cluster_no = 0
            for dire_in_okayd in first_layers:
                #print "DIRE_IN=", dire_in_okayd
                if dire_in_okayd.rfind("cluster_") != -1:
                    #print dire_in_okayd
                    cluster_no=int(dire_in_okayd.split("cluster")[1].replace("_","").split("/")[0])
                    #print "cluster_no=", cluster_no
                    if max_cluster_no < cluster_no:
                        max_cluster_no = cluster_no
                        join_path = os.path.join(okay_dir, dire_in_okayd)
            max_cluster_dirs.append(join_path)

        # HTML file of KAMO merging 
        # Selected directories 'okay_dirs' were already selected.
        self.html_reports = []
        for okay_dir in okay_dirs:
            # Check existence 
            html_file_path = os.path.join(okay_dir, "report.html")

            # If the 'report.html' exists in the designated directory
            if os.path.exists(html_file_path) == True:
                relpath = os.path.relpath(html_file_path)
                print "HHHHHHHHHHHHTTTTTTTTTTTTTTTMMMMMMMMMMMMMMLLLLLLLLLLL=", relpath
                self.html_reports.append(relpath)
            else:
                continue

        self.final_dires = []
        # Searching the maximum number of run
        for cluster_dir in max_cluster_dirs:
            #print "FINAL_PROCESSING=%s" % cluster_dir
            dp=DirectoryProc.DirectoryProc(cluster_dir)
            third_layers = dp.findDirs()

            max_run = 0
            for sec_dir in third_layers:
                #print "PROCESSING=", sec_dir
                if sec_dir.rfind("run") != -1:
                    try:
                        run_no = int(sec_dir.replace("run_",""))
                        if run_no > max_run:
                            max_run = run_no
                            join_dir = os.path.join(cluster_dir, sec_dir)
                            #print "JOJOJOJO=",join_dir
                            self.final_dires.append(join_dir)
                    except:
                        print "Something wrong in directory name: %s " % sec_dir

        return self.final_dires

    def findReflectionFile(self, final_dires, file_list = ["XSCALE.LP", "XSCALE.INP", "aniso.log", "pointless.log"], isIncludeMTZ=True):
        self.reflection_related_files = []
        saved_dir = ""
        xscale_list = []
        for data_root in final_dires:
            if isDebug: print "D=", data_root
            if saved_dir == data_root:
                if isDebug: print "IDENTICAL!!!!"
                continue
            else:
                saved_dir = data_root

            for check_file in file_list:
                check_path = os.path.join(data_root, check_file)
                if os.path.exists(check_path) == True:
                    relpath = os.path.relpath(check_path)
                    self.reflection_related_files.append(relpath)
                    if relpath.rfind("XSCALE.LP") != -1:
                        xscale_list.append(data_root)
            # MTZ file
            if isIncludeMTZ == True:
                mtz_path = os.path.join(data_root, "ccp4/xscale.mtz")
                mtz_relpath = os.path.relpath(mtz_path)
                self.reflection_related_files.append(mtz_relpath)

        print self.reflection_related_files

    def getArchiveFileList(self):
        arc_files = []

        arc_files += self.html_reports
        arc_files += self.reflection_related_files

        return arc_files
        
    # This is the latest version at BL32XU 2020/02/18
    def makeReportMerge(self, prefix="archive", option = "NO"):
        if self.isPrep == False:
            self.prep()

        # preparing everything
        #unko = Unko.Unko(self.root_dir)
        okay_dirs = self.getListOfGoodMergeDirs()
        final_dirs = self.findFinalResultsDir(okay_dirs)
        tt.findReflectionFile(final_dirs, file_list = ["XSCALE.LP", "XSCALE.INP", "aniso.log", "pointless.log"])
        filelist = self.getArchiveFileList()

        return filelist

    def makeMessage(self, filelist):
        if len(filelist) != 0:
            mail_comments = "\nY=Y=Y=Y=Y=Y=Y=Y E-MAIL REPORT BODY Y=Y=Y=Y=Y=Y=Y=Y=Y=Y\n"

            mail_comments += "Datasets were merged by using KAMO automerge.\n"
            mail_comments += "Please refer merging statistics by browsing following html.\n"
            for html_report in self.html_reports:
                mail_comments += "%s\n" % os.path.relpath(html_report)

            mail_comments += "\nX=X=X=X=X=X=X= An attached archive files =X=X=X=X=X=X=X=X=X\n"
            mail_comments += "= This archive file includes followings.\n"
            if isIncludeMTZ == True:
                mail_comments += "Reflection files are indluded.\n"
            else:
                mail_comments += "Reflection files are not included.\n"

            for targetdir in self.final_dires:
                mail_comments += "%s\n" % os.path.relpath(targetdir)

            mail_comments += "\nZ=Z=Z=Z=Z=Z=Z=Z=Z=Z Explanations Z=Z=Z=Z=Z=Z=Z=Z=Z=Z=Z=Z=Z=Z"
            mail_comments += "\n= _final/ is a final result of KAMO auto merge.\n"
            mail_comments += "= The resolution limit of the directory was determined automatically.\n"
            mail_comments += "= The resolution limit was defined by CC(1/2)~50% in XSCALE.LP in\n"
            mail_comments += "= 'cluster' with the 'largest' number of datasets.\n"
            mail_comments += "= We are sending only the cluster results with the largest number of merged datasets.\n"
            mail_comments += "= Please check 'other' clusters after you get your HDD backup.\n"
            mail_comments += "= You can overview all of results in 'html' file for each sample.\n"
            mail_comments += "= Hierarchical clustering: cell parameter based -> BLEND (merge_blend_*) \n"
            mail_comments += "= Hierarchical clustering: CC intensity based -> cc (merge_ccc_*) \n"
            mail_comments += "= If the directory name is 'merge_blend_3.0S_SAMPLENAME/'\n"
            mail_comments += "= a clustering is conducted in 'cell parameter based' method.'\n"
            mail_comments += "= Starting resolution limit for merging is 3.0A resolution.'\n"
            mail_comments += "= 'KAMO automerge' estimates resolution limit by CC(1/2) for each dataset.\n"
            mail_comments += "= If the resolution value is lower than 'starting resolution limit', KAMO \n"
            mail_comments += "= restarts XSCALE process after setting'lower resolution value' in XSCALE.INP.\n"
            mail_comments += "= In this manner, resolution limit is defined by the program.\n"
            mail_comments += "= The string '_final' in the directory path has a meaning of 'final resolution limit'.\n"
            mail_comments += "= SAMPLENAME should be identical to the name defined in ZOOPREP.csv file.\n\n"
            mail_comments += "= Please contact us if you have any questions. \n"
            mail_comments += "= Kunio Hirata (Corresponding developer of ZOO system): kunio.hirata@riken.jp \n"

        else:
            return "Nothing"

        return mail_comments

    def makeArchiveFileMerge(self):
        if len(all_list) != 0:
            # Making archive commend
            da = MyDate.MyDate()
            dstr = da.getNowMyFormat(option="other")

            tgz_file = "%s_%s.tgz " % (dstr, prefix)
            print tgz_file

            command = "tar cvfz %s" % tgz_file
            for good_file in all_list:
                if isDebug: print "GOOD",good_file
                command += "%s " % good_file

            while(1):
                if os.path.isfile(tgz_file) == False:
                    print "waiting for %s" % tgz_file
                    break
                    time.sleep(1)
                else:
                    os.path.getsize(tgz_file)
                    break

            # Send mail
            #command = "cat message.txt | mailx -a %s -s \"ZOO report .tgz is attached [%s]\" kunio.hirata@riken.jp" % (tgz_file, tgz_file)
            #os.system(command)
            ############################################################

            os.system(command)
        else:
            print "No good merged results."

if __name__ == "__main__":
    tt = Unko(".")
    option = sys.argv[1]
    prefix = sys.argv[2]

    #def makeReportMerge(self, prefix="archive", option = "NO"):
    filelist = tt.makeReportMerge("archive_test", option = "NO")
    mail_comment = tt.makeMessage(filelist)
    print mail_comment

    filelist = tt.makeArchiveLargeWedge()
    print "large_wedge=",filelist

    """
    if option == "kamo_large":
        print "KKKKKKKKKKKKKKKKKKKKKKKKKKKKKK"
        filelist = tt.makeArchiveLargeWedge()
        da = MyDate.MyDate()
        dstr = da.getNowMyFormat(option="other")
        command = "tar cvfz %s_%s.tgz " % (dstr, prefix)
        for arc_each in filelist:
            command += "%s " % arc_each
        print command
        os.system(command)
            
    else:
        print "JJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJ"
        prefix = sys.argv[2]
        tt.makeReportMerge(prefix, "include_mtzfiles")
    """
