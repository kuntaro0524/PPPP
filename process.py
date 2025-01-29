import subprocess

print subprocess
#subprocess.call(['ls','-l'],shell=True)
#output=subprocess.check_output(['ls','-l'],shell=True)
for i in dir(subprocess):
	print i
#output = subprocess.check_output(['ls', '-1'])

