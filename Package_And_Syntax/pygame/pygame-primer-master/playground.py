import pygame
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((800,600))

# Variable to keep our main loop running
running = True

# Our main loop!
while running:
    # for loop through the event queue
    for event in pygame.event.get():
        # Check for KEYDOWN event; KEYDOWN is a constant defined in pygame.locals, which we imported earlier
        if event.type == KEYDOWN:
            # If the Esc key has been pressed set running to false to exit the main loop
            if event.key == K_ESCAPE:
                running = False
        # Check for QUIT event; if QUIT, set running to false
        elif event.type == QUIT:
            running = False

surf = pygame.Surface((50,50))
surf.fill((255,255,255))
rect = surf.get_rect()
#
screen.blit(surf, (400,300))
pygame.display.flip()