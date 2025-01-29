import sys
import struct
import Numeric, Image

class Image:
	def __init__(self,filename):
		self.filename=filename

		# rayonix detector
                little       = "<"
                tiff         = "1024s"
                title_header = "1L16s39L80s"
                data_sta     = "11L84s"
                more_sta     = "128H"
                gonio        = "28l16s"
                detec        = "8l96s"
                opti         = "10l16s10l16s16s"
                file_para    = "128s128s64s32s32s32s512s96s"
                dataset      = "512s"
                pad          = "512x"
                self.mar = little + tiff + title_header + data_sta + \
                           more_sta + gonio + detec + opti + file_para + dataset + pad


	def readImage(self):
		file=open(self.filename,"rb")
		self.raw_header=file.read(4096)

		self.body=file.read(3072*3072*2)
		file.close()

		header=struct.unpack(self.mar,self.raw_header)

                self.distance  = float(header[183])  / 1000
                self.osc_range = float(header[207])  / 1000
                self.osc_start = float(header[191])  / 1000
                self.wavelength = float(header[224]) / 100000
                self.axis_num  = header[206]
                self.beam_x = float(header[184])  / 1000
                self.beam_y = float(header[185])  / 1000

                if self.axis_num == 4:
                        self.axis = "Omega"
                else:
                        self.axis = "UNKNOWN"

		return self.body

	def array2image(self,a):
		if a.typecode()==Numeric.UnsignedInt8:
			mode="L"
		elif a.typecode()==Numeric.Float32:
			mode="F"
		else:
			raise ValueError, "unsupported image mode"
		return Image.fromstring(mode,(a.shape[1],a.shape[0]),a.tostring())

if __name__=="__main__":
	img=Image(sys.argv[1])

	body=img.readImage()

	newi=img.array2image(body)
