import sys,os

lines = open(sys.argv[1],"r").readlines()

cwd = os.getcwd()
print cwd

for line in lines:
    print os.path.join(cwd, line).strip(),",EmbA,no"
