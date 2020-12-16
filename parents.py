from config import *
import pygame


class Sprite(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0, size=TILE_SIZE, speed=0, image=PLAYER_ASSETS['idle']):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.speed = speed
        self.x = x
        self.y = y
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)
