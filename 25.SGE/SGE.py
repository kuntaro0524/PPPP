import subprocess

class SGE():
    def __init__(self):
        self.isPrep = True
#print subprocess
#output = subprocess.call(['qstat'],shell=True)
output = subprocess.check_output(['qstat'],shell=True)

# column 1: ID, 5: run status

lines = output.split("\n")
icount = 0
for line in lines:
    cols = line.split()

    if len(cols) == 8:
        job_id = int(cols[0])
        command = "qstat -j %s | grep cwd" % job_id
        output2 = subprocess.check_output(command, shell = True)
        print job_id,output2,
        icount += 1

print "Number of jobs = ",icount
