import time
import string
import random

# PyGame Constants
import pygame
from pygame.locals import *
from pygame.color import THECOLORS

import box

def main():
    WINSIZE = 640,480
    pygame.init()
    screen = pygame.display.set_mode(WINSIZE,0,8)
    pygame.display.set_caption('Bouncing Baby Boxes!')
    
    screen.fill(THECOLORS["black"])
    
    box1 = box.Box( screen, (32,32), (1,1), THECOLORS["black"], THECOLORS["white"] )
    box2 = box.Box( screen, (32,32), (-1,-1), THECOLORS["black"], THECOLORS["red"])
    box3 = box.Box( screen, (32,32), (1, 4), THECOLORS["black"], THECOLORS["green"])
    # The Main Event Loop
    done = False
    while not done:
        # Drawing:
        box1.draw()
        box2.draw()
        box3.draw()
        # Drawing finished this iteration?  Update the screen
        pygame.display.update()
            
        # Event Handling:
        events = pygame.event.get( )
        for e in events:
            if( e.type == QUIT ):
                done = True
                break
            elif (e.type == KEYDOWN):
                if( e.key == K_ESCAPE ):
                    done = True
                    break
                if( e.key == K_f ):
                    pygame.display.toggle_fullscreen()

    print "Exiting!"

    return
if __name__=="__main__":
    main()
    
