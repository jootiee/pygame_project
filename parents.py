from config import *
import pygame as pg


class Sprite(pg.sprite.Sprite):
    def __init__(self, x=0, y=0, size=TILE_SIZE, speed=0, image=MISSING):
        pg.sprite.Sprite.__init__(self)
        self.size = size
        self.speed = speed
        self.image = pg.image.load(image)
        self.image = pg.transform.scale(self.image, (self.size, self.size))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)