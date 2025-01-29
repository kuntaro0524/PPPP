import sys,os,math
import h5py
from yamtbx.dataproc import eiger
from yamtbx.dataproc import cbf
from yamtbx.dataproc.XIO.plugins import eiger_hdf5_interpreter
from libtbx import easy_mp
import glob

class ProcHD5:
	def __init__(self,masterfile,nread):
		self.masterfile=masterfile
		self.nread=nread

	def test(self):
		data=None
		sel=None
		nimage=0
		print "Processing %s %d"%(self.masterfile,self.nread)
		self.body = eiger.extract_data(self.masterfile, self.nread, apply_pixel_mask=False)
		print "Dimensions=",self.body.shape

	def setCenter(self,beamx,beamy):
		self.beamx=beamx
		self.beamy=beamy

	def returnIndex(self,dist):
		#print "distance=",dist
		for i in range(0,self.ncols):
			lower_limit=i*self.step
			upper_limit=i*self.step+self.step
			#print lower_limit,upper_limit
			if dist>=lower_limit and dist<=upper_limit:
				return i

	def returnRange(self,index):
		lower_limit=index*self.step
		upper_limit=index*self.step+self.step
		average=(lower_limit+upper_limit)/2.0

		return average

	def calcCircle(self,radius_limit,pix_div):
		self.step=pix_div
		# Making column
		column_list=[]
		column_limit=[]
		self.ncols=int(float(radius_limit)/float(pix_div))+1

		value_list=[0]*self.ncols
		npix_list=[0]*self.ncols
		medium_list=[0]*self.ncols

		for j in range(0,self.ncols):
			medium_list[j]=self.returnRange(j)

		for v in range(0,self.body.shape[0]):
			for h in range(0,self.body.shape[1]):
				pcx=v-self.beamy
				pcy=h-self.beamx
				dist_pix=math.sqrt(pcx*pcx+pcy*pcy)

				# Pixel far from the length limit
				if dist_pix > radius_limit:
					continue

				# Pixel in blind region
				if self.body[v][h] < 0:
					continue

				idx=self.returnIndex(dist_pix)
				value_list[idx]+=int(self.body[v][h])
				npix_list[idx]+=1

		outfile=self.masterfile.replace(".h5",".dat")
		of=open(outfile,"w")

		for value,npix,med in zip(value_list,npix_list,medium_list):
			if npix!=0:
				average=float(value)/float(npix)
				of.write("%10.2f %10.2f\n"%(med,average))
				#print med,average
		of.close()

	def merge(self,conds):
                master_file,startnum,endnum,cbfile=conds
		endnum=endnum
		print "Processing %s %d %d"%(master_file,startnum,endnum)
		data=None
		sel=None
		nimage=0
		for i in range(startnum,endnum+1):
			print "Processing %s %d"%(master_file,i)
			tmp = eiger.extract_data(master_file, i, apply_pixel_mask=False)
			print "Extracging"
			if data is None: data = tmp
			else:
				data += tmp
		if sel is None: sel = tmp < 0
		else: sel |= tmp < 0
		data[sel] = -10

		frameno=0

		print "DONE LOOP"
		h = eiger_hdf5_interpreter.Interpreter().getRawHeadDict(master_file)
		h5 = h5py.File(master_file, "r")

		h["Detector"] = h5["/entry/instrument/detector/description"].value
		h["ExposurePeriod"] = h5["/entry/instrument/detector/frame_time"].value
		cbf.save_numpy_data_as_cbf(data.flatten(), size1=data.shape[1], size2=data.shape[0], title="merged_%d"%frameno,
                             cbfout=cbfile,
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

if __name__=="__main__":
	ph=ProcHD5(sys.argv[1])
	ph.test()
	ph.setCenter(1554.7,1597.8)
	ph.calcCircle(1000,25)
