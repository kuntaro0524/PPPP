import sys,os,math
import AttFactor

att=AttFactor.AttFactor()
option=sys.argv[1]

startphi=float(sys.argv[1])
endphi=float(sys.argv[2])
stepphi=float(sys.argv[3])
exptime=float(sys.argv[4])

total_phi=endphi-startphi
nframe=int(total_phi/stepphi)

print "total osc range:",total_phi," deg."
print "# of frames    :",nframe
total_exp=exptime*nframe
print "Total exposure:",exptime*nframe

print ">>>>> 0.5 sec life time <<<<<"
rotspd=total_phi/total_exp
trans=0.5/total_exp
print "10x10um beam: %8.2f"%(trans*100)," %"
thick=att.calcThickness(1.0,trans)
print "Thickness %8.2f"%thick,"[um]"
print "Rot speed %8.3f"%rotspd,"[deg/sec]"

print "\n>>>>> 1.0 sec life time <<<<<"
trans=1.0/total_exp
print "10x10um beam: %8.2f"%(trans*100)," %"
thick=att.calcThickness(1.0,trans)
print "Thickness %8.2f"%thick,"[um]"
print "Rot speed %8.3f"%rotspd,"[deg/sec]"
