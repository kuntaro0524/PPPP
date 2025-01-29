import os,sys,path

class StatusFile:
    def __init__(self, proc_dire, proc_tag):
        self.proc_dire = os.path.abspath(proc_dire)
        self.proc_tag = proc_tag
        # Start file
        self.start_file = ".START_%s" % proc_tag
        # Processing file
        self.processing_file = ".PROCESSING_%s" % proc_tag
        # Finish file
        self.finished_file = ".FINISHED_%s" % proc_tag

    def checkStatus(self):
        possible_filenames = [self.start_file, self.processing_file, self]

    def markStart(self):
        start_file = os.path.join(self.proc_dir,proc_tag)
        ofile = open(start_file,"w")
