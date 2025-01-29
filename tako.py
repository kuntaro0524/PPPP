import os,sys,math,numpy
import numpy
import AttFactor

if len(sys.argv)!=4:
	print "Usage: tako.py CRY_SIZE[um] OSC[deg] TOTAL_OSC[deg]"
	sys.exit(1)

Lc=float(sys.argv[1])
phid=float(sys.argv[2])
phit=float(sys.argv[3])

flux=1.3E13
Bv=18.0
exp=0.1

# 10MGy
lim_ph=1.0E10

att_fac=(lim_ph*Lc*Bv*phid)/(flux*exp*phit)

afac=AttFactor.AttFactor()
print "Beam vertical size = 18.0 um, exposure=0.1sec "
print "Suggested attenuation thickness=%8.1f [um]"%afac.calcThickness(1.0,att_fac)
