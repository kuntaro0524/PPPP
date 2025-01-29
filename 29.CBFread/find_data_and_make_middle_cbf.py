import os,sys,math
import ResultsZOO

proc_dire=sys.argv[1]

ddd=ResultsZOO.ResultsZOO(proc_dire)
sch_files,sch_paths=ddd.getScheudlePaths("_kamoproc_restart")

print sch_files

for sch_file,sch_path in zip(sch_files,sch_paths):
    print "PROCESSING",sch_file
    if sch_file.rfind("multi")!=-1:
        ddd.procMultiDS(sch_file,sch_path)
    elif sch_file.rfind("cry")!=-1:
        ddd.procHelical(sch_file,sch_path)
