import sys
import datetime
from MyException import *
import Image
import ImageDraw,ImageFont
from myfont import fontPath


class BeamCenter:

	def __init__(self,filename):
		self.filename=filename

	def countSaturated(self):
		im=Image.open(self.filename)
		newi=im.convert("L")
		pix=newi.load()
		
		cnt=0

		for x in range(0,im.size[0]):
			for y in range(0,im.size[1]):
				if pix[x,y]>=240:
					cnt+=1

		return cnt

	def find2(self):
		im=Image.open(self.filename)
		newi=im.convert("L")
		pix=newi.load()

		# size=(width,height)

		sumpeak=0.0


	# Average
		for x in range(0,im.size[0]):
			for y in range(0,im.size[1]):
				if pix[x,y]<=255:
					sumpeak+=pix[x,y]

		npix=im.size[0]*im.size[1]
		ave=sumpeak/float(npix)

		print ave

	# Threshold
		thresh=ave*3.0
		sumpeak=0.0
		sumx=0.0
		sumy=0.0
		for x in range(0,im.size[0]):
			for y in range(0,im.size[1]):
				if pix[x,y]>thresh:
					sumpeak+=pix[x,y]
					sumx+=pix[x,y]*x
					sumy+=pix[x,y]*y

		# Exception
		if sumpeak==0.0:
			raise MyException("Beam monitor did not catch your beam!!")

		cenx=sumx/sumpeak
		ceny=sumy/sumpeak

		# output log image
		draw=ImageDraw.Draw(im)

		# drawing circle at calculated position
		draw.ellipse((cenx-5,ceny-5,cenx+5,ceny+5),fill=(0,0,0))

		# Date
		dstr="%s"%datetime.datetime.now()
		font=ImageFont.truetype(fontPath,14)

		str2="Pixel    (Y,Z)=(%8.2f,%8.2f)[pix]"%(cenx,ceny)

		# um convertion
		yum=cenx*5.0/67.0
		zum=ceny/26.75

		str3="Position (Y,Z)=(%8.3f,%8.3f)[um]"%(yum,zum)

		draw.text((10,400),dstr,font=font)
		draw.text((10,420),str2,font=font)
		draw.text((10,440),str3,font=font)
		
		newfile=self.filename.replace(".ppm","_ana.png")
		im.save(newfile,"PNG")

		return(cenx,ceny)

	def find(self):
		im=Image.open(self.filename)
		newi=im.convert("L")
		pix=newi.load()

		# size=(width,height)

		sumpeak=0.0

	# Average
		for x in range(0,im.size[0]):
			for y in range(0,im.size[1]):
				if pix[x,y]<=255:
					sumpeak+=pix[x,y]

		npix=im.size[0]*im.size[1]
		ave=sumpeak/float(npix)

		print ave

	# Threshold
		thresh=ave*3.0
		sumpeak=0.0
		sumx=0.0
		sumy=0.0
		for x in range(0,im.size[0]):
			for y in range(0,im.size[1]):
				if pix[x,y]>thresh:
					sumpeak+=pix[x,y]
					sumx+=pix[x,y]*x
					sumy+=pix[x,y]*y

		# Exception
		if sumpeak==0.0:
			raise MyException("Beam monitor did not catch your beam!!")

		cenx=sumx/sumpeak
		ceny=sumy/sumpeak

		# output log image
		draw=ImageDraw.Draw(im)

		# drawing circle at calculated position
		draw.ellipse((cenx-5,ceny-5,cenx+5,ceny+5),fill=(0,0,0))

		# Date
		dstr="%s"%datetime.datetime.now()
		font=ImageFont.truetype(fontPath,14)

		str2="Pixel    (Y,Z)=(%8.2f,%8.2f)[pix]"%(cenx,ceny)

		# um convertion
		yum=cenx*5.0/67.0
		zum=ceny/26.75

		str3="Position (Y,Z)=(%8.3f,%8.3f)[um]"%(yum,zum)

		draw.text((10,400),dstr,font=font)
		draw.text((10,420),str2,font=font)
		draw.text((10,440),str3,font=font)
		
		newfile=self.filename.replace(".ppm","_ana.png")
		im.save(newfile,"PNG")
		
		return cenx,ceny


if __name__=="__main__":
	p=BeamCenter(sys.argv[1])

	print p.countSaturated()
	#print p.find2()
