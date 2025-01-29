import numpy as n


for phi in n.arange(0,360,10):
	phi_rad=n.radians(phi)
	print "%7.2f %8.3f"%(phi,n.cos(phi_rad))
