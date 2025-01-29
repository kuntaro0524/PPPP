import h5py
from yamtbx.dataproc import eiger
from yamtbx.dataproc import cbf
from yamtbx.dataproc.XIO.plugins import eiger_hdf5_interpreter
from libtbx import easy_mp
from PIL import Image
import PIL.ImageOps 
import numpy
import glob

def run(paramlist):
  masterfile,startnum,endnum,outf=paramlist
  frameno=10
  data = None
  sel = None
  nimage=0

  for i in range(startnum,endnum):
     print "summing up %5d"%i
     tmp = eiger.extract_data(masterfile, i, apply_pixel_mask=False)
     if data is None: data = tmp
     else:
       data += tmp
       #sel = tmp >= 0
       #data[sel] += tmp[sel]
       #print data
  if sel is None: sel = tmp < 0
  else: sel |= tmp < 0

  data[sel] = -10

  h = eiger_hdf5_interpreter.Interpreter().getRawHeadDict(masterfile)
  h5 = h5py.File(masterfile, "r")

  h["Detector"] = h5["/entry/instrument/detector/description"].value
  h["ExposurePeriod"] = h5["/entry/instrument/detector/frame_time"].value
  cbf.save_numpy_data_as_cbf(data.flatten(), size1=data.shape[1], size2=data.shape[0], title="merged_%d"%frameno,
                             cbfout=outf,
                             pilatus_header="""\
# Detector: %(Detector)s, S/N %(SerialNumber)s
# Pixel_size %(PixelX)e m x %(PixelY)e m
# %(SensorMaterial)s sensor, thickness %(SensorThickness).3e m
# Exposure_time %(ExposureTime).6f s
# Exposure_period %(ExposurePeriod).6f s
# Count_cutoff %(Overload)d counts
# Wavelength %(Wavelength).6f A
# Detector_distance %(Distance).3e m
# Beam_xy (%(BeamX).1f, %(BeamY).1f) pixels
# Start_angle %(PhiStart).6f deg.
# Angle_increment %(PhiWidth).6f deg.
""" % h)

  d=data.flatten()
  size1,size2= data.shape
  #print size1,size2
  rsd=d.reshape(size1,size2)
  pil_img=Image.fromarray(numpy.uint8(rsd))
  reimage=pil_img.resize((800,800))
  pngname=outf.replace(".cbf",".png")
  #reimage=PIL.ImageOps.invert(reimage)
  reimage.save(pngname)
  
if __name__ == "__main__":
  import sys

  master_file=sys.argv[1]
  startnum=int(sys.argv[2])
  endnum=int(sys.argv[3])
  num_of_merge=int(sys.argv[4])

  n_frames=endnum-startnum+1
  n_block=int(n_frames/num_of_merge)

  print "NUM OF MERGE = ",n_frames
  print "NUM OF BLOCK = ",n_block

  proc_list=[]
  for i in range(0,n_block):
	bl_start=i*num_of_merge+1
	bl_end=bl_start+num_of_merge-1
	block_id=i+1
	filename="merged_%05d.cbf"%block_id
	proc_list.append((master_file,bl_start,bl_end,filename))

  print proc_list
  print "making %05d files"%len(proc_list)
  easy_mp.pool_map(fixed_func=lambda n: run(n), args=proc_list, processes=8)
