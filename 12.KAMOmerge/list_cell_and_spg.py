import os,sys
sys.path.append("/isilon/BL32XU/BLsoft/PPPP")
import AnaCORRECT
import DirectoryProc

if __name__=="__main__":
    dp=DirectoryProc.DirectoryProc(sys.argv[1])
    dlist=dp.getDirList()
    #print dp.findTargetFileIn(sys.argv[1],"CORRECT.LP")
    targetlist,pathlist=dp.findTargetFileInTargetDirectories("./","CORRECT.LP")

    #print targetlist
    for targetfile in targetlist:
        ac=AnaCORRECT.AnaCORRECT(targetfile)
        a,b,c,alpha,beta,gamma = ac.getCellParm()
        spg = ac.getFinalSPG()
        print a,b,c,alpha,beta,gamma,spg
