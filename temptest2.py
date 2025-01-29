from TemplateMatch import *
import sys

templf=sys.argv[1]
#z+000um.ppm
#z-001um.ppm
#z-002um.ppm
#z-003um.ppm
#z-004um.ppm

ofile="z+000um.ppm"
tm=TemplateMatch(templf,ofile)
z0=tm.getXY()[1]
tm.show()

ofile="z-001um.ppm"
tm=TemplateMatch(templf,ofile)
z1=tm.getXY()[1]
tm.show()

ofile="z-002um.ppm"
tm=TemplateMatch(templf,ofile)
z2=tm.getXY()[1]
tm.show()

ofile="z-003um.ppm"
tm=TemplateMatch(templf,ofile)
z3=tm.getXY()[1]
tm.show()

ofile="z-004um.ppm"
tm=TemplateMatch(templf,ofile)
z4=tm.getXY()[1]
tm.show()

print z0,z1,z2,z3,z4

#phi000.ppm  phi000_10um_up.ppm  phi000_5um_up.ppm
