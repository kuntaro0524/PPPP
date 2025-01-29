import os,sys
beamx_imos=float(sys.argv[1]) # vertical
beamy_imos=float(sys.argv[2]) # horizontal

vpix=3269
hpix=3110

hori_ratio=beamy_imos/233.2
vert_ratio=beamx_imos/245.2

print hori_ratio*hpix
print vert_ratio*vpix
