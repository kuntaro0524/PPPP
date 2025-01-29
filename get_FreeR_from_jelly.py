import os,sys
import FileString

if __name__=="__main__":

        fs=FileString.FileString(sys.argv[1])

        frstr="****                Things for loggraph, R factor and others                ****"
        tostr="****                      Fom and SigmaA vs resolution                      ****"

        search_table=fs.extractFromTo(frstr,tostr)
        fs.makePlot(search_table,0,11,sys.argv[2])
