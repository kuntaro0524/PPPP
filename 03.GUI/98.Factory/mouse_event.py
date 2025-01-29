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
pythonImg = pygame.image.load("circle_small.png").convert_alpha()

cur_pos = (0,0)    # centering circle position
pythons_pos = []   # copy list of circle

while True:
    screen.blit(backImg, (0,0))
    
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        # Mouse click : save position 
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
	# which button?
 	    print event.type
            x, y = event.pos
            x -= pythonImg.get_width() / 2
            y -= pythonImg.get_height() / 2
            pythons_pos.append((x,y))  # Add circle 
	    print x,y
        # Mouse click : save position 
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos
            x -= pythonImg.get_width() / 2
            y -= pythonImg.get_height() / 2
            pythons_pos.append((x,y))  # Add circle 
	    print x,y
        # moving circle
        if event.type == MOUSEMOTION:
            x, y = event.pos
            x -= pythonImg.get_width() / 2
            y -= pythonImg.get_height() / 2
            cur_pos = (x,y)
	    print x,y
    
    # 蛇を表示
    screen.blit(pythonImg, cur_pos)
    for i, j in pythons_pos:
        screen.blit(pythonImg, (i,j))
    
    pygame.display.update()
