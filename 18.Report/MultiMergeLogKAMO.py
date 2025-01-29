import os,sys
sys.path.append("/isilon/BL45XU/BLsoft/PPPP/")
sys.path.append("/isilon/BL45XU/BLsoft/PPPP/18.Report/")

import DirectoryProc

class MultiMergeLogKAMO():
    def __init__(self, multi_merge_log):
        self.multi_merge_log = multi_merge_log
        self.isRead = False
        self.isdone = False

    def readLog(self):
        self.lines = open(self.multi_merge_log, "r").readlines()
        self.isRead = True

    def isDone(self):
        if self.isRead == False:
            self.readLog()
    
        proc_flag = 0
        for line in self.lines:
            if line.rfind("Normal exit at") != -1:
                self.isDone = True

        return self.isDone

    def checkStatus(self):
        if self.isRead == False:
            self.readLog()
    
        proc_flag = 0
        for line in self.lines:
            if line.rfind("ERROR: No clusters satisfied the specified conditions for merging!") != -1:
                proc_flag = 1001

        return proc_flag

dp = DirectoryProc.DirectoryProc("./")
merge_dires = dp.findDirsWithName("merge_")

ofile = open("send_data.csv","w")
for merge_dir in merge_dires:
    dpdp = DirectoryProc.DirectoryProc(merge_dir)
    logpaths, procpaths = dpdp.findTarget("multi_merge.log")

    for logpath,procpath in zip(logpaths,procpaths):
        mlog = MultiMergeLogKAMO(logpath)
        isdone = mlog.isDone()
        if isdone == True:
            print "ok_dir:",logpath,mlog.checkStatus()
            ofile.write("%s\n" % procpath)

ofile.close()
