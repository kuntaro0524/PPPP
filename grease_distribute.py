import Device
import datetime

host = '172.24.242.41'
port = 10101

dev=Device.Device(host)
dev.init()

# Travel between Z-limits 
# Beam stopper Z cannot be moved beyond the collision position
# with the back light

print datetime.datetime.now()

for i in range(0,100):
#while True:
#	dev.colli.travelLimit2Limit()
#	dev.bs.travelLimit2Limit()
	dev.bm.travelLimit2Limit()
	print "%d times" %i

print datetime.datetime.now()
