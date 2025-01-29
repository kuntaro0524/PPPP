import sys
import socket
import time
import math
from numpy import *
from AttFactor import *

if __name__=="__main__":
	att=AttFactor()
	print len(sys.argv)

	wave=float(sys.argv[1])

	while(1):
		# Values from KUMA
		print "(KUMA estimation is based on 1.0sec exposure)"
		print "KUMA: Suggested thickness:"
		thick=float(raw_input())
		print "KUMA: input oscillation width? (deg/frame):"
		osc=float(raw_input())
		print "Input parameters"
		print "Al thickness=%8.1f[um] Oscillation %5.1f[deg/frame]" % (thick,osc)
		print "is it ok?"
		com=raw_input()
		if com=="" or com=="y" or com=="Y" or com=="yes" or com=="YES":
			break

	################################
	# Condition osc. exp. trans
	#   KUMA     a    b    trans_KUMA
	#  Desired   d    e    trans_Desi
	# ---------------------------
	# rate_KUMA = a/b [deg./sec.] 
	# rate_Desi = d/e [deg./sec.] 
	# ---------------------------
	# ratio = (d/e) / rate_KUMA
	# trans(Desi) = trans_KUMA * ratio
	#################################

	# rate(KUMA)
	rate_KUMA=osc/1.0

	# Transmission of KUMA value
	trans_KUMA=att.calcAttFac(wave,thick)
	print "KUMA transmission %5.1f percent"%(trans_KUMA*100.0)

	for exptime in arange(0.1,1.0,0.1):
		# Exposure time with the same exposure ratio
		ratio=(osc/exptime)/rate_KUMA
		#print "RATIO",ratio
		trans_Desi=trans_KUMA*ratio
		print "%5.1f [sec] transmission: %10.1f percent"%(exptime,trans_Desi*100),
		att_Desi=att.calcThickness(wave,trans_Desi)
		print "%10.3f[um]"%att_Desi,
		if att_Desi < 0.0:
			print "Impossible"
		else:
			print ""
