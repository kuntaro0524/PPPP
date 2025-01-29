import sys,os
import socket
sys.path.append("/isilon/BL32XU/BLsoft/PPPP/")

from AnalyzePeak import *
from Att import *

host = '172.24.242.41'
port = 10101
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))

if len(sys.argv)!=4:
	print "Usage: this ENERGY AIMED_DOSE DOSE_PER_SEC"
	sys.exit()

energy=float(sys.argv[1])
aimed_dose=float(sys.argv[2])
dose_per_sec=float(sys.argv[3])

wl=12.3984/energy

exp_for_aimed_dose=aimed_dose/dose_per_sec


trans_probe_dose=exp_for_aimed_dose/100.0

attfac=Att(s)
althick=attfac.getBestAtt(wl,trans_probe_dose)
trans_selected_al=attfac.calcAttFac(wl,althick)
exp_probe=trans_probe_dose/trans_selected_al


# 1ko usui Al
althick_new=attfac.getAttBefore(althick)
trans_selected_al_new=attfac.calcAttFac(wl,althick_new)
exp_probe_new=trans_probe_dose/trans_selected_al_new

print "###############################"
print "Aimed dose %4.1f MGy : Exposure time: %4.2f sec"%(aimed_dose,exp_for_aimed_dose)
print "Probe measurement condition : 0.3 MGy Al thick %4d [um] Exp.time %4.2f [sec]"%(althick,exp_probe)
print "Probe measurement condition : 0.3 MGy Al thick %4d [um] Exp.time %4.2f [sec]"%(althick_new,exp_probe_new)
print "###############################"
