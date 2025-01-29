#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import sys

SCREEN_SIZE = (640, 480)

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption(u"Centering circle")

backImg = pygame.image.load("image000.ppm").convert()
circleImg = pygame.image.load("circle_small.png").convert_alpha()

cur_pos = (0,0)    # centering circle position
circlePos = []   # copy list of circle
linePos=[]

fo=open("test.dat","w")

while True:

    for event in pygame.event.get():
	if event.type==QUIT:
		pygame.quit()
		sys.exit()

    screen.blit(backImg, (0,0))
    
    x,y=pygame.mouse.get_pos()
    x -= circleImg.get_width() / 2
    y -= circleImg.get_height() / 2
    print x,y
    cur_pos=(x,y)


    mouse_pressed=pygame.mouse.get_pressed()

    if mouse_pressed[0]:
        x,y=pygame.mouse.get_pos()
        x -= circleImg.get_width() / 2
        y -= circleImg.get_height() / 2
        circlePos.append((x,y))  # Add circle
    	fo.write("CIRCLE: %5d %5d\n"%(x,y))

    if mouse_pressed[2]:
        print "RIGHT"
        #idx=len(circlePos)
	break
        #print idx
        #circlePos.remove(idx-1)

    if mouse_pressed[1]:
	ndata=len(circlePos)
	#print "ndata %8d\n"%ndata
	print circlePos

	# Choose line points
	tmp=(0,0) 
        tmp2=(100,100)
	if ndata==0:
		pygame.draw.line(screen, (255,255,255), tmp, tmp2)
	#for p in range(0,len(circlePos)):
		#tmp=
	
    	for i, j in circlePos:
		i+=circleImg.get_width()/2
		j+=circleImg.get_width()/2
		pygame.draw.line(screen, (255,255,255), (i,j), (640,480))

    # display circle
    screen.blit(circleImg, cur_pos)
    #print len(circlePos)
    for i, j in circlePos:
       	screen.blit(circleImg, (i,j))
    pygame.display.update()
