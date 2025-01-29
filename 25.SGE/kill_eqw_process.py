import subprocess

output = subprocess.check_output(['qstat'],shell=True)

lines = output.split("\n")
n_error = 0
error_job_list = ""
for line in lines:
    cols = line.split()

    if len(cols) == 8:
        job_id = int(cols[0])
        istate = cols[4]
        #print job_id, istate
        if istate == "Eqw":
            n_error += 1
            error_job_list += " %d"%job_id

if n_error != 0:
    print "Number of jobs = ",error_job_list
    command = "qdel %s" % error_job_list
    output = subprocess.check_output([command],shell=True)
else:
    print "No error jobs"
