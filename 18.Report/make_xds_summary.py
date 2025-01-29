import sys,os
sys.path.append("/isilon/BL32XU/BLsoft/PPPP/")
import glob,numpy
import DirectoryProc
import AnaCORRECT

# Finding xscale.mtz
dp=DirectoryProc.DirectoryProc(os.environ["PWD"])
corrlp_list,path_list=dp.findTarget("CORRECT.LP")

# Log file
logf=open("correct.txt","w")

exec_dir = os.path.abspath("../../")

print corrlp_list
corrlp_list.sort()
print corrlp_list

# find CORRECT.LP and analyze
for corrlp in corrlp_list:
    print corrlp
    ac=AnaCORRECT.AnaCORRECT(corrlp)
    total_rmeas=ac.getTotalRmeas()
    #if total_rmeas > 0.0:
        #print corrlp
    #compl,redun,outer_rmeas,outer_isigi=ac.getOuterShellInfo()
    compl,redun,rmeas,isigi,cchalf = ac.getOuterShellInfo()

    nds= ac.countDatasets()
    #print compl,redun,outer_rmeas,outer_isigi,nds
    #lines=ac.getStatsTable()
    lines=ac.getStatsTableAsItIs()

    logf.write("###########################\n")
    #relpath = os.path.relpath(exec_dir, corrlp)
    relpath = os.path.relpath(corrlp, exec_dir)
    print relpath
    logf.write("%s\n"%relpath)
    for line in lines:
        logf.write("%s"%line)
