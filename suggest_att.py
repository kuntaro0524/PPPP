import sys
import socket
import time
import math
from AttFactor import *

if __name__=="__main__":

	att=AttFactor()

	if (len(sys.argv)!=4):
		print "Usage: this WAVELENGTH DOSE_FF DOSE_DESIRED"
		sys.exit(1)

	wave=float(sys.argv[1])
	ff_dose=float(sys.argv[2])
	desired_dose=float(sys.argv[3])

	attfac=desired_dose/ff_dose

	thickness=att.calcThickness(wave,attfac)

	print "Suggested attenuator=%8.1f[um]"%thickness
