#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import sys
 
SCREEN_SIZE = (640, 480)
 
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption(u"figure")
 
while True:
    screen.fill((0,0,0))

    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    backImg = pygame.image.load("image008.ppm").convert()
    screen.blit(backImg, (0,0))
    pygame.display.set_caption(u"Centering circle")

    # 図形を描画
    pygame.draw.rect(screen, (255,255,0), Rect(10,10,300,200))     # 黄の矩形
    #pygame.draw.circle(screen, (255,0,0), (320,240), 100)          # 赤の円
    #pygame.draw.ellipse(screen, (255,0,255), (400,300,200,100))    # 紫の楕円
    #pygame.draw.line(screen, (255,255,255), (0,0), (640,480))      # 白い線
    
    screen.blit(backImg, (0,0))
    #pygame.display.update()

    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
