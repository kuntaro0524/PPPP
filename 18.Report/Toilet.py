import os, sys, math, numpy, scipy, glob
import Unko

sys.path.append("/isilon/BL32XU/BLsoft/PPPP/10.Zoo/Libs/")
sys.path.append("/isilon/BL32XU/BLsoft/PPPP/10.Zoo/Libs/")

import ZOOreporter
import MyDate
import XDSReporter
import DirectoryProc

class Toilet:
    def __init__(self, zoo_path, report_prefix):
        self.zoo_path = zoo_path
        self.prefix = report_prefix

    def makeHTML(self):
        # Finding all zoo.db files
        zoo_files = glob.glob("%s/*db" % self.zoo_path)

        # Size check and go
        if len(zoo_files) == 0:
            print "No zoo.db files"
            return 

        html_files = []
        index = 0
        for zoo_file in zoo_files:
            zoo_size = os.path.getsize(zoo_file)
            prefix_html = "%s_%02d" % (self.prefix, index)
            if zoo_size < 1000:
                print "Too small: Skipped %s" % zoo_size
            else:
                zrp = ZOOreporter.ZOOreporter(zoo_file, beamline="BL32XU")
                html_files.append(zrp.makeHTML(prefix_html))
            index += 1

        return html_files

    def makeReflectionArchive(self, option):
        # Default directory to be checked
        kamodir = "%s/_kamoproc/" % self.zoo_path
        kamo_abs_path = os.path.abspath(kamodir)
        #print "KAMOKAMO= ", kamo_abs_path
        # searching zoo.db files
        unko = Unko.Unko(kamo_abs_path)

        if option == "kamo_large":
            #print "KAMO_LARGE KAMO_LARGE"
            filelist = unko.makeArchiveLargeWedge()
            return filelist

        else:
            print "Option is unknown."

    # 2020/02/28 K.Hirata
    # Roughly completed in 'large wedge data collection'
    def makeAllArchive(self):
        # Archive file prefix
        da = MyDate.MyDate()
        dstr = da.getNowMyFormat(option="min")
        arc_file = "%s_%s.tgz" % (dstr, self.prefix)
        command = "tar cvfz %s " % arc_file

        # HTML file about data collection in ZOO
        html_files = self.makeHTML()
        for html_file in html_files:
            html_file_rel = os.path.relpath(html_file, "./")
            command += "%s " % html_file_rel

        # Large wedge reflection files -> .tgz file
        reflection_files = self.makeReflectionArchive("kamo_large")
        for arc_each in reflection_files:
            command += "%s " % arc_each

        # XDSreporter for large wedge
        tmp_kamo = "%s/_kamoproc/" % self.zoo_path
        abs_kamo = os.path.abspath(tmp_kamo)
        xdsr = XDSReporter.XDSReporter(abs_kamo)
        xdsr.makeHTML()
        xds_report_html = os.path.relpath("%s/correct.html" % abs_kamo, "./")
        xds_report_src = os.path.relpath("%s/contents/" % abs_kamo, "./")

        # Merge directory
        # _kamo directories
        dp = DirectoryProc.DirectoryProc(self.zoo_path)
        dires = dp.findDirs()

        for each_dir in dires:
            archive_index = 0
            if each_dir.rfind("_kamo") != -1:
                abs_kamo = os.path.abspath(os.path.join(self.zoo_path, each_dir))

                unko = Unko.Unko(abs_kamo)
                # Merging directories with '_final' results
                okay_dirs = unko.getListOfGoodMergeDirs()
                # Find directories with final merging calculations
                final_dirs = unko.findFinalResultsDir(okay_dirs)
                unko.findReflectionFile(final_dirs, file_list = ["XSCALE.LP", "XSCALE.INP", "aniso.log", "pointless.log"])
                files_from_merge = unko.getArchiveFileList()
                archive_index += 1

                for each_file in files_from_merge:
                    command += "%s " % each_file

        # Archive all HTML files 
        command += "%s " % html_file_rel
        command += "%s " % xds_report_html
        command += "%s " % xds_report_src

        # Executing the command
        os.system(command)

if __name__ == "__main__":

    zoo_path = sys.argv[1]
    report_prefix = sys.argv[2]

    print zoo_path, report_prefix
    print "NUMBER OF ARGUMENTS=", len(sys.argv)
    if len(sys.argv) != 3:
        print "Usage: toilet.py ZOO_PATH REPORT_PREFIX"
        sys.exit()

    toilet = Toilet(zoo_path, report_prefix)
    toilet.makeAllArchive()
        
    # Making HTML file to view data collectio results
    # def __init__(self, zoo_path, report_prefix):
    # Making reflection list
    #toilet.makeReflectionArchive("kamo_large")

