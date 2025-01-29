import subprocess

def better_impl(cmd):
    print "start better_impl %s" % cmd
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print "waiting"
    stdout_data, stderr_data = p.communicate()
    print "finish: %d %d" % (len(stdout_data), len(stderr_data))
    return p.returncode, stdout_data, stderr_data

command1 = "phenix.refine ./free.mtz ./1lyz_prot.pdb"
better_impl(command1)
