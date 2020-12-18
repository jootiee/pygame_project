from config import *
from player import *
import pygame as pg


class Screen_damage(Sprite):
    def __init__(self, x=0, y=0, size=50, speed=0, image=MISSING):
        Sprite.__init__(self, x, y, size, speed, image)
        # print(type(self.image))
        self.image = pg.transform.scale(self.image, (WIN_SIZE[0], WIN_SIZE[1]))
        self.player = Player()

    def update(self):
        if self.player.taking_damage:
            self.image = MISSING
        else:
            self.image = BLANK_SCREEN

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)
