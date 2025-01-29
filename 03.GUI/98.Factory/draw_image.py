#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import sys

SCREEN_SIZE = (640, 480)

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption(u"drawing image")

# イメージを用意
backImg = pygame.image.load("image000.ppm").convert()     # 背景
pythonImg = pygame.image.load("z-5um.ppm").convert_alpha()  # 蛇

while True:
    screen.blit(backImg, (0,0))        # 背景を描画
    screen.blit(pythonImg, (320,400))  # 蛇を描画
    pygame.display.update()
    
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
