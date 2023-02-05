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

def initClientSocket():

    def clientSocketReader(clientSocket):
        print("Reader thread started")
        while(True):
            try:
                data = clientSocket.recv(1024)
                if not data:
                    break
                else:
                    print(data)
            except:
                print("Reader thread stopped")
                break
    
    def clientSocketWriter(clientSocket):
        print("Writer thread started")
        try:
            while(True):
                playerPos = str(player.rect.x) + "," + str(player.rect.y)
                data = pickle.dumps(playerPos)
                clientSocket.sendall(data)
                time.sleep(0.1)
        except:
            print("Writer thread stopped")
            return


    HOST = "127.0.0.1"  # The server's hostname or IP address
    PORT = 5555  # The port used by the server
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((HOST, PORT))
    socketWriterThread = threading.Thread(target=clientSocketWriter, args=(clientSocket,))
    socketWriterThread.setDaemon(True)
    return (clientSocket, socketWriterThread)



if __name__ == "__main__":
    pygame.init()
    clock = pygame.time.Clock()
    
    # Set up the drawing window
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    
    player = Player()

    clientSocket, socketWriterThread = initClientSocket()
    socketWriterThread.start()

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

        # Update the player sprite based on user keypresses
        player.update(pressed_keys)


        # Fill the background with white
        screen.fill((0, 0, 0))

        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)

        # Flip the display
        pygame.display.flip()

        deltaTime = clock.tick(GAME_TICK_SPEED)

    # Done! Time to quit.
    clientSocket.close()
    pygame.quit()