import time
import math
import socket
import pygame
import threading
import pickle
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

from misc import *
from network import NetworkInterface



if __name__ == "__main__":
    pygame.init()
    # Set up the drawing window
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    clock = pygame.time.Clock()
    
    # Initialize network interface
    networkInterface = NetworkInterface()
    response = networkInterface.connect()
    if response is None:
        pygame.quit()
        exit(0)
    networkInterface.id = response
    print(f"Client id: {networkInterface.id}")

    # Initialize player instance
    player = Player()

    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    # Run until the user asks to quit
    running = True
    while running:
        
        # Did the user click the window close button?
        for event in pygame.event.get():
            # Did the user hit a key?
            if event.type == KEYDOWN:
                # Was it the Escape key? If so, stop the loop.
                if event.key == K_ESCAPE:
                    running = False
            # Did the user click the window close button? If so, stop the loop.
            elif event.type == QUIT:
                running = False

        # Get all the keys currently pressed
        pressed_keys = pygame.key.get_pressed()

        # Fill the background with white
        screen.fill((0, 0, 0))

        # Update the player sprite based on user keypresses
        player.update(pressed_keys)

        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)

        # Flip the display
        pygame.display.flip()

        # Calculate deltaTime ... needs work
        deltaTime = clock.tick(GAME_TICK_SPEED)

    # Done! Time to quit.
    networkInterface.close()
    pygame.quit()