import pygame as pg
import random
import os
import math

from config import *
from player import *
from props import *
from hud import *
from camera import *


class Game:

    def __init__(self):
        pg.init()
        self.display = pg.display.set_mode(WIN_SIZE)
        self.clock = pg.time.Clock()
        self.background = pg.image.load(BACKGROUND)
        self.background = pg.transform.scale(self.background, WIN_SIZE)
        self.running = True
        self.down = self.up = self.left = self.right = False
        self.played = 0.0
        self.player_created = False
        self.level = 0
        self.player = Player()
        self.screen_damage = Screen_damage()
        self.load_map()

    # method for first load/reload sprites
    def load_sprites(self):
        self.objects = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.spikes = pg.sprite.Group()
        self.medkits = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.solid_blocks = pg.sprite.Group()
        self.hud = pg.sprite.Group()
        self.hud.add(self.screen_damage)
        Player.coins = self.coins
        Player.spikes = self.spikes
        Player.medkits = self.medkits
        Player.solid_blocks = self.solid_blocks
        self.camera = Camera(self.player, self.objects)

    # restarts the game, resets player stats
    def restart(self):
        self.level = 0
        self.player = Player()
        self.load_map()

    # loads map from /lvl/
    def load_map(self):
        self.load_sprites()
        map_path = LEVELS[self.level]
        with open(map_path, encoding='utf-8') as file:
            for y, line in enumerate(file):
                for x, letter in enumerate(line):
                    if letter in MAP.keys():
                        pos = x * TILE_SIZE, y * TILE_SIZE
                        image = MAP[letter]
                        if letter == 'R':
                            block = self.player
                            block.set_position(*pos)
                        if letter in SOLID_BLOCKS:
                            block = Sprite(*pos, image=image)
                            self.solid_blocks.add(block)
                        if letter == 'S':
                            block = Spike(*pos, image=image)
                            self.spikes.add(block)
                        elif letter == 'C':
                            block = Coin(*pos, value=5, image=image)
                            self.coins.add(block)
                        self.objects.add(block)
        self.camera.update_borders()


    # game run
    def run(self):
        while self.running:
            self.events()
            self.update()
            self.render()

    # events catch
    def events(self):
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_s:
                    self.down = True
                if event.key == pg.K_w:
                    self.up = True
                if event.key == pg.K_a:
                    self.left = True
                if event.key == pg.K_d:
                    self.right = True
                if event.key == pg.K_r:
                    self.restart()
            if event.type == pg.KEYUP:
                if event.key == pg.K_s:
                    self.down = False
                if event.key == pg.K_w:
                    self.up = False
                if event.key == pg.K_a:
                    self.left = False
                if event.key == pg.K_d:
                    self.right = False
                if event.key == pg.K_ESCAPE:
                    self.running = False

    # updates the screen
    def update(self):
        ms = self.clock.tick(FPS)
        self.played += ms / 1000
        pg.display.set_caption(
            f"Player's money: {self.player.money}. Player's hp: {self.player.hp} Played: {self.played:.2f}")
        self.camera.update()
        self.player.update(self.up, self.down, self.left, self.right, ms)
        self.coins.update()
        self.hud.update()

        if not self.coins:
            if self.level < len(LEVELS) - 1:
                self.level += 1
            self.load_map()

    def render(self):
        self.display.blit(self.background, (0, 0))
        self.objects.draw(self.display)
        self.hud.draw(self.display)
        pg.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()
    pg.quit()
