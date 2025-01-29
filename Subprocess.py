import subprocess

class Subprocess:
    def __init__(self):
        self.procs=[]

    def proc(self,command,option):
        p = subprocess.Popen([command, option],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                shell=False)
        self.procs.append(p)
        print 'return: %d' % (p.wait(), )
        print 'stdout: %s' % (p.stdout.readlines(), )
        print 'stderr: %s' % (p.stderr.readlines(), )

    def communicates(self):
        print self.procs
        for proc in self.procs:
            output=proc.communicate()[0]
            print output

    def proc_180626(self,command):
        #print "proc!"
        coms= command.split()
        print coms
        try:
            retcode=subprocess.check_call(coms)
        except subprocess.CalledProcessError as e:
            print "Exception",e
            #print e.returncode
            #print e.cmd
            #print e.output

        print type(retcode)
        #for r in retcode:
            #print r
        #print retcode

    def proc_communicate(self,command):
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
        print "Waiting"
        stdout_data, stderr_data = p.communicate()
        print "finished %d %d"%(len(stdout_data),len(stderr_data))
        return p.returncode, stdout_data, stderr_data

if __name__=="__main__":
    sp=Subprocess()
    #sp.proc("csh","long.csh")
    #sp.proc("csh","long2.csh")
    #sp.communicates()

    com="mtzdmp ccp4/free.mtz"
    #sp.proc_180626(com)
    rc,st,err=sp.proc_communicate(com)

    for i in st.split("\n"):
        if i.rfind("Free")!=-1 or i.rfind("free")!=-1:
            if i.rfind(" I ")!=-1:
                cols=i.split()
                for col in cols: 
                    if col.rfind("free")!=-1 or col.rfind("Free")!=-1:
                        print col
