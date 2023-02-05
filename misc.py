import pygame
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

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GAME_TICK_SPEED = 60

class Player(pygame.sprite.Sprite):
    
    def __init__(self, velocity=2, x=0, y=0):
        super(Player, self).__init__()
        self.surf = pygame.Surface((50, 50))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocity = velocity

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -self.velocity)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, self.velocity)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-self.velocity, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(self.velocity, 0)
        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT