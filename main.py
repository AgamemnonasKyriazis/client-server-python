import time
import math
import sys
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


def update_server():
    global running, local_sprites, remote_sprites
    t0 = time.time_ns()
    while running:
        t1 = time.time_ns()
        if abs(t1 - t0) >= 10000:
            t0 = time.time_ns()
            response = networkInterface.send({networkInterface.id: [entity.rect for entity in local_sprites]})
            if response is not None:
                remote_sprites.empty()
                for client_key, rect_list in response.items():
                    if client_key != networkInterface.id:
                        for rect in rect_list:
                            remote_sprites.add(Entity(rect))




if __name__ == "__main__":
    pygame.init()
    # Set up the drawing window
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    clock = pygame.time.Clock()
    
    # Initialize network interface
    networkInterface = NetworkInterface(host="loukoumades.ddns.net", port=7777)
    response = networkInterface.connect()
    if response is None:
        pygame.quit()
        exit(0)
    networkInterface.id = response
    print(f"Client id: {networkInterface.id}")

    # Initialize player instance
    player = Player()

    local_sprites = pygame.sprite.Group()
    remote_sprites = pygame.sprite.Group()
    local_sprites.add(player)

    # Run until the user asks to quit
    running = True
    network_thread = threading.Thread(target=update_server)
    network_thread.start()
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

        #networkInterface.send(all_sprites)
        

        for entity in local_sprites:
            screen.blit(entity.surf, entity.rect)

        for entity in remote_sprites:
            screen.blit(entity.surf, entity.rect)

        # Flip the display
        pygame.display.flip()

        # Calculate deltaTime ... needs work
        deltaTime = clock.tick(GAME_TICK_SPEED)

    # Done! Time to quit.
    network_thread.join()
    networkInterface.close()
    pygame.quit()