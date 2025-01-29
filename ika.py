import os,sys,math,numpy
import numpy
import AttFactor

if len(sys.argv)!=3:
	print "Usage: tako.py OSC[deg] TOTAL_OSC[deg]"
	sys.exit(1)

phid=float(sys.argv[1])
phit=float(sys.argv[2])

Lc=13

flux=1.3E13
Bv=18.0
exp=0.1

# 10MGy
lim_ph=1.0E10

att_fac=(lim_ph*Lc*Bv*phid)/(flux*exp*phit)

afac=AttFactor.AttFactor()
print "Beam vertical size = 18.0 um, exposure=0.1sec "
print "Suggested attenuation thickness=%8.1f [um]"%afac.calcThickness(1.0,att_fac)
