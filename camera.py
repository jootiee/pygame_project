from config import *
from player import *


class Camera:
    def __init__(self, player, borders):
        self.player = player
        self.blocks = borders

    def update_borders(self):
        self.top = self.left = self.right = self.bottom = self.player
        for block in self.blocks:
            if block.rect.top < self.top.rect.top:
                self.top = block
            if block.rect.bottom > self.bottom.rect.bottom:
                self.bottom = block
            if block.rect.left < self.left.rect.left:
                self.left = block
            if block.rect.right > self.right.rect.right:
                self.right = block

    def update(self):
        w, h = WIN_SIZE
        x, y = self.player.rect.center
        dx = -(self.player.rect.x + self.player.rect.w // 2 - w // 2)
        dy = -(self.player.rect.y + self.player.rect.h // 2 - h // 2)

        if self.top.rect.top + dy > 0:
            dy = -self.top.rect.top
        if self.bottom.rect.bottom + dy < h:
            dy = h - self.bottom.rect.bottom
        if self.left.rect.left + dx > 0:
            dx = -self.left.rect.left
        if self.right.rect.right + dx < w:
            dx = w - self.right.rect.right

        # if x < 0.2 * w:
        #     dx = -self.player.speed_x
        # if x > 0.8 * w:
        #     dx = -self.player.speed_x
        # if y < 0.2 * h:
        #     dy = -self.player.speed_y
        # if y > 0.8 * h:
        #     dy = -self.player.speed_y


        for block in self.blocks:
            if block.animated:
                block.rect = block.rect.move(dx, 0)
                block.spawn = (block.spawn[0], block.spawn[1] + dy)
            else:
                block.rect = block.rect.move(dx, dy)
