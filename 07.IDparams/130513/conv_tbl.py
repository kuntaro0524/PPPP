#!/bin/env python
import os
import sys
import socket
import time
import datetime
import math
import socket
import pylab
import scipy
import numpy
from pylab import *
from scipy.interpolate import splrep,splev,interp1d,splprep


if __name__=="__main__":

  cols=[]

  fname = sys.argv[1]
  oname = "id32xu.tbl"
  bssname = "id32xu.bss"

  f = open(fname,"r")
  lines = f.readlines()
  f.close()
  for line in lines:
        if line.strip().find("#")==0:
                continue
        new=[]
        new=line.replace(","," ").strip().split()

        cols.append(new)

        ncols=len(cols)
        #print self.ncols

  xdat=[]
  ydat=[]

  for idx in range(0,ncols):
        xdat.append(float(cols[idx][0]))
        ydat.append(float(cols[idx][3]))

  xd=pylab.array(xdat)
  yd=pylab.array(ydat)

  otbl = open(oname,"w")
  obss = open(bssname,"w")
  for i in range(0,ncols):
    otbl.write("%8.3f %10.5f\n" % (xd[i],yd[i]))
    obss.write("_energy_vs_gap:%8.3f %10.5f\n" % (xd[i],yd[i]))

  otbl.close

