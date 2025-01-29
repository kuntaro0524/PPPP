import sys
from Gonio import *

# server open
#host = '192.168.163.1'
host = '172.24.242.41'
port = 10101
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))

## Gonio
gonio=Gonio(s)

print "1st point: X Y Z [mm]"
point1=raw_input().split()

if len(point1)!=3:
	print "Input error"
	sys.exit(1)

print "2nd point: X Y Z [mm]"
point2=raw_input().split()

if len(point2)!=3:
	print "Input error"
	sys.exit(1)

cenx=(float(point1[0])+float(point2[0]))/2.0
ceny=(float(point1[1])+float(point2[1]))/2.0
cenz=(float(point1[2])+float(point2[2]))/2.0

dx=float(point1[0])-cenx
dy=float(point1[1])-ceny
dz=float(point1[2])-cenz

diffdist=math.sqrt(dx*dx+dy*dy+dz*dz)

print "============================"
print "============================"
print "CENTER: %9.4f %9.4f %9.4f"%(cenx,ceny,cenz)
print "Diff from origin = %8.4f[mm]"%diffdist
print "============================"
print "============================"

print "Move to the position? (y/n) [enter:no]"
answer=raw_input()

if answer=="y":
	gonio.moveXYZmm(cenx,ceny,cenz)
