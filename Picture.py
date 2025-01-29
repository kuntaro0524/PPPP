import sys
import math
import datetime
from MyException import *
import Image
import ImageDraw,ImageFont
import pygame
from pygame.locals import *
from myfont import fontPath

LEFT=1
RIGHT=2

SCREEN_SIZE=(700,500)


class Picture:

	def __init__(self,filename):
		self.filename=filename

	def getGreyPix(self):
		self.im=Image.open(self.filename)
		self.newi=self.im.convert("L")
		self.pix=self.newi.load()
		
	def summed(self):
		self.getGreyPix()
		
		total=0
		for x in range(0,self.im.size[0]):
			for y in range(0,self.im.size[1]):
				total+=self.pix[x,y]
	
		print total
		return total

	def drawLineOnPicture(self):
                pygame.init()

                self.screen = pygame.display.set_mode(SCREEN_SIZE)
                pygame.display.set_caption(u"Picture test")
                self.backImg = pygame.image.load(self.filename).convert()
                self.circleimg = pygame.image.load("637px-Star_Ouro.svg.png").convert_alpha()

                self.cur_pos = (0,0)    # centering circle position
                self.cir_pos = []   # copy list of circle

		while True:
			self.screen.blit(self.backImg, (0,0))
    			for event in pygame.event.get():
        			if event.type == QUIT:
            				sys.exit()
        			# Mouse click : save position 
        			if event.type == MOUSEBUTTONDOWN and event.button == 1:
            				x, y = event.pos
            				x -= self.circleimg.get_width() / 2
            				y -= self.circleimg.get_height() / 2
            				self.cir_pos.append((x,y))  # Add circle 

        			# Mouse click : RIGHT button
        			if event.type == MOUSEBUTTONDOWN and event.button == 3:
					print self.cir_pos
					return self.cir_pos, self.cx,self.cy

        			# Mouse click : MIDDLE button
        			if event.type == MOUSEBUTTONDOWN and event.button == 2:
            				tmp=(0,0)

        			# moving circle
        			if event.type == MOUSEMOTION:
            				x, y = event.pos
            				x -= self.circleimg.get_width() / 2
            				y -= self.circleimg.get_height() / 2
            				self.cur_pos = (x,y)
	    				#print x,y
    
    			# Displaying circle
    			self.screen.blit(self.circleimg, self.cur_pos)
    			#print self.cir_pos
    			for i, j in self.cir_pos:
        			self.screen.blit(self.circleimg, (i,j))

    			cen_totx=0
    			cen_toty=0

    			for p in range(0,len(self.cir_pos)):
				cenx1=self.cir_pos[p-1][0]+self.circleimg.get_width()/2
				ceny1=self.cir_pos[p-1][1]+self.circleimg.get_height()/2
				cenx2=self.cir_pos[p][0]+self.circleimg.get_width()/2
				ceny2=self.cir_pos[p][1]+self.circleimg.get_height()/2
			# average center
				cen_totx+=self.cir_pos[p][0]+self.circleimg.get_width()/2
				cen_toty+=self.cir_pos[p][1]+self.circleimg.get_height()/2

       				pygame.draw.line(self.screen, (255,255,255), (cenx1,ceny1), (cenx2,ceny2))
				print "%5d %5d %5d"%(p,cen_totx,cen_toty)

    			ndata=len(self.cir_pos)
    			if ndata!=0:
				print ndata
    				self.cx=int(cen_totx/ndata)
    				self.cy=int(cen_toty/ndata)
    				pygame.draw.circle(self.screen, (255,255,255), (self.cx,self.cy), 10,1)

    			pygame.display.update()

	def getYprofileInX(self,cenx):
		self.getGreyPix()
		
		for y in range(0,self.im.size[1]):
			print self.pix[cenx,y]
				
	def contrast(self):
		im=Image.open(self.filename)
		newi=im.convert("L")
		pix=newi.load()
		
		cnt=0

		min=99999
		max=-99999
		for x in range(0,im.size[0]):
			for y in range(0,im.size[1]):
				if pix[x,y]>10:
					if pix[x,y]<min:
						min=pix[x,y]
					if pix[x,y]>max:
						max=pix[x,y]

		#print min,max
		print max-min

	def maxEnt(self):
		im=Image.open(self.filename)
		newi=im.convert("L")
		pix=newi.load()
		
		total=0
		cnt=0

		for x in range(0,im.size[0]):
			for y in range(0,im.size[1]):
				total+=pix[x,y]

		total_ent=0.0

		for x in range(0,im.size[0]):
			for y in range(0,im.size[1]):
				value=pix[x,y]
				if value!=0:
					normalized_pix=float(value)/float(total)
					ent=normalized_pix*math.log(normalized_pix)
						
					total_ent+=ent

		print -total_ent
		#print min,max
		##print max-min

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
	p=Picture(sys.argv[1])

	p.drawLineOnPicture()
	#p.getYprofileInX(int(sys.argv[2]))
	#p.summed()
	#p.maxEnt()
	#p.contrast()
	#print p.find2()
