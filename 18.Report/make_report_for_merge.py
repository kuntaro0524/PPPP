import sys,os
sys.path.append("/isilon/BL32XU/BLsoft/PPPP/")
sys.path.append("/isilon/BL32XU/BLsoft/PPPP/11.ClusterAnalysis/")
import glob,numpy
import DirectoryProc
import MyDate
import time
import XSCALEReporter
# DEBUG flag
isDebug = False
isIncludeMTZ = False

# directories where merge was proceeded.
dp = DirectoryProc.DirectoryProc(".")
merge_dires = dp.findDirsWithName("merge_")

prefix = sys.argv[1]

if len(sys.argv) == 3:
    option = sys.argv[2]
else:
    option = "NO"

if option.rfind("include") != -1:
    isIncludeMTZ = True

# Check paths as 'absolute' paths
abs_paths = []

for merge_dir in merge_dires:
    abs_path = os.path.abspath(merge_dir)
    abs_paths.append(abs_path)
    print "MERGE=", abs_path

okay_dirs = []
data_roots = []
html_reports = []

# For 'merge' directories
for check_path in abs_paths:
    # Finding 'final' directories in designated paths
    dp=DirectoryProc.DirectoryProc(check_path)
    dirs=dp.findTargetDirs("final")

    # No final directories -> skipped
    if len(dirs) == 0:
        if isDebug: print "Skipping ", check_path
        continue

    else:
        pass
        #print "CHECKPOINT1=", check_path
    # Searching *html file of KAMO merging report.
    html_files, paths_list = dp.findTarget("report.html")

    if len(html_files) != 0:
        for html_report in html_files:
            #print "TTTTTTTTTTTTTTTTT",html_report
            if html_report.rfind("_final") == -1:
                continue
            else:
                relpath = os.path.relpath(html_report)
                html_reports.append(relpath)

    # Finding a cluster with the largest number of merged datasets
    max_cluster_no=0
    maxd = -9999

    # dirs: all merging directories with name '_final'
    for d in dirs:
        # Find 'run_01, run_02, run_03' directories
        if d.rfind("run_")!=-1:
            cluster_no=int(d.split("cluster")[1].replace("_","").split("/")[0])
            # The largest number of 'run' is required.
            if cluster_no > max_cluster_no:
                max_cluster_no=cluster_no
                maxd=d
                isFoundRun = True
                final_d = d

    if maxd == -9999:
        print "Merging process was not proceeded in %s" % check_path
        continue

    max_cluster_d=maxd.split("run_")[0]
    dp=DirectoryProc.DirectoryProc(max_cluster_d)

    rundirs= dp.findTargetDirs("run")

    if len(data_roots) == 0:
        data_roots.append(final_d)
    else:
        if isDebug:
            print "<<<<<"
            print data_roots
            print "=>>"
        for data_root in data_roots:
            if isDebug:
                print "####################"
                print "COMPARE(fin   )=", final_d
                print "COMPARE(Stored)=", data_root
            if final_d == data_root:
                if isDebug: print "Identical!!!"
                continue
            if isDebug: print "STORED:", final_d
            data_roots.append(final_d)
            break

if isDebug:
    for d in data_roots:
        print "DDD=", d

check_list = ["XSCALE.LP", "XSCALE.INP", "aniso.log", "pointless.log"]

all_list = []
saved_dir = ""
xscale_list = []
for data_root in data_roots:
    if isDebug: print "D=", data_root
    if saved_dir == data_root:
        if isDebug: print "IDENTICAL!!!!"
        continue
    else:
        saved_dir = data_root

    for check_file in check_list:
        check_path = os.path.join(data_root, check_file)
        if os.path.exists(check_path) == True:
            relpath = os.path.relpath(check_path)
            all_list.append(relpath)
            if relpath.rfind("XSCALE.LP") != -1:
                xscale_list.append(data_root)
    # MTZ file
    if isIncludeMTZ == True:
        mtz_path = os.path.join(data_root, "ccp4/xscale.mtz")
        mtz_relpath = os.path.relpath(mtz_path)
        all_list.append(mtz_relpath)

#HTML FILE
for html_report in html_reports:
    #print "TTTTTTTTTT ==%s=="%html_report
    all_list.append(html_report)

# Making XSCALE results
#reporter = XSCALEReporter.XSCALEReporter(xscale_path)
#reporter.makeHTML(figdpi=65)

# Making archive commend
da = MyDate.MyDate()
dstr = da.getNowMyFormat(option="other")

tgz_file = "%s_%s.tgz " % (dstr, prefix)
print tgz_file

command = "tar cvfz %s" % tgz_file
for good_file in all_list:
    if isDebug: print "GOOD",good_file
    command += "%s " % good_file

#print command
os.system(command)

mail_comments = "\nY=Y=Y=Y=Y=Y=Y=Y E-MAIL REPORT BODY Y=Y=Y=Y=Y=Y=Y=Y=Y=Y\n"

mail_comments += "Datasets were merged by using KAMO automerge.\n"
mail_comments += "Please refer merging statistics by browsing following html.\n"
for html_report in html_reports:
    mail_comments += "%s\n" % os.path.relpath(html_report)

mail_comments += "\nX=X=X=X=X=X=X= An attached archive files =X=X=X=X=X=X=X=X=X\n"
mail_comments += "= This archive file includes followings.\n"
if isIncludeMTZ == True:
    mail_comments += "Reflection files are indluded.\n"
else:
    mail_comments += "Reflection files are not included.\n"

for targetdir in data_roots:
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

ofile = open("message.txt", "w")
for line in mail_comments:
    ofile.write("%s" % line)

ofile.close()

while(1):
    if os.path.isfile(tgz_file) == False:
        print "waiting for %s" % tgz_file
        break
        time.sleep(1)
    else:
        os.path.getsize(tgz_file)
        break


# Send mail
command = "cat message.txt | mailx -a %s -s \"ZOO report .tgz is attached [%s]\" kunio.hirata@riken.jp" % (tgz_file, tgz_file)
os.system(command)