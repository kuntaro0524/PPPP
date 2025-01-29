import os,sys,math,glob
import time
import DirectoryProc
import AnaCORRECT
import XDSascii
import Fitting
import AnaDSlog

if __name__ == "__main__":
        dp=DirectoryProc.DirectoryProc(sys.argv[1])
        list1= dp.findTargetFileInRoot(sys.argv[3])
