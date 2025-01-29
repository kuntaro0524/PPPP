#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import sys

LEFT=1
RIGHT=2

SCREEN_SIZE = (640, 480)

## for this main
sys.path.append("/isilon/BL32XU/BLsoft/PPPP/")
import socket
from Gonio import *

from Capture import *

class PointCry:

	def __init__(self,cryimg):
		pygame.init()
		self.screen = pygame.display.set_mode(SCREEN_SIZE)
		pygame.display.set_caption(u"Centering circle")
		self.backImg = pygame.image.load(cryimg).convert()
		self.circleimg = pygame.image.load("circle_small.png").convert_alpha()

		self.cur_pos = (0,0)    # centering circle position
		self.cir_pos = []   # copy list of circle

	def ppp(self):
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
					pygame.display.quit()
					return self.cx,self.cy

        			# Mouse click : MIDDLE button
        			if event.type == MOUSEBUTTONDOWN and event.button == 2:
					self.cir_pos=[]

        			# moving circle
        			if event.type == MOUSEMOTION:
            				x, y = event.pos
            				x -= self.circleimg.get_width() / 2
            				y -= self.circleimg.get_height() / 2
            				self.cur_pos = (x,y)
	    				print x,y
    
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


	def drawBack(self):
		self.screen.blit(self.backImg,(0,0))

	def drawCircle(self,imgfile,code):

		self.drawBack()
       		#pygame.draw.line(self.screen, (255,255,255), (10,10), (20,20))

		while(True):
    			for event in pygame.event.get():
        			if event.type == MOUSEBUTTONDOWN and event.button == 3:
					return(1)
    			pygame.draw.circle(self.screen, (255,255,255), code, 10,1)
    			pygame.display.update()

if __name__ == "__main__":

        host = '172.24.242.41'
        port = 10101
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host,port))

	cap=Capture()
	gonio=Gonio(s)
	gonio.rotatePhi(0)

	ofile="/isilon/users/target/target/Staff/test.ppm"
	cap.capture(ofile)
	#cap.disconnect()

	ttt=PointCry(ofile)
	pn,cx,cy=ttt.ppp()
	print cx,cy
	zero_code=(cx,cy)
	ttt.drawCircle(ofile,zero_code)

	# rotate phi
	gonio.rotatePhi(90)
	ofile="/isilon/users/target/target/Staff/test.ppm"
	cap.capture(ofile)

	ttt=PointCry(ofile)
	pn,cx,cy=ttt.ppp()
	print cx,cy
	vert_code=(cx,cy)
	ttt.drawCircle(ofile,vert_code)
