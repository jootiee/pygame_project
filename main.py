import pygame
import random
import os
import math


# импорт констант + загрузка ассетов
from config import *
from player import *
from props import *


class Game:
    def __init__(self):
        pygame.init()
        self.display = pygame.display.set_mode(WIN_SIZE)
        self.clock = pygame.time.Clock()
        self.background = pygame.image.load(BACKGROUND)
        self.background = pygame.transform.scale(self.background, WIN_SIZE)
        self.running = True
        self.down = self.up = self.left = self.right = False
        self.played = 0.0
        self.player_created = False
        self.level = 0
        self.player = Player()
        self.load_map()

    def load_sprites(self):
        self.objects = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.spikes = pygame.sprite.Group()
        self.medkits = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.solid_blocks = pygame.sprite.Group()
        Player.coins = self.coins
        Player.spikes = self.spikes
        Player.medkits = self.medkits
        Player.solid_blocks = self.solid_blocks

    def restart(self):
        self.level = 0
        self.player = Player()
        self.load_map()

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

    def run(self):
        while self.running:
            self.events()
            self.update()
            self.render()

    def events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    self.down = True
                if event.key == pygame.K_w:
                    self.up = True
                if event.key == pygame.K_a:
                    self.left = True
                if event.key == pygame.K_d:
                    self.right = True
                if event.key == pygame.K_r:
                    self.restart()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_s:
                    self.down = False
                if event.key == pygame.K_w:
                    self.up = False
                if event.key == pygame.K_a:
                    self.left = False
                if event.key == pygame.K_d:
                    self.right = False
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def update(self):
        ms = self.clock.tick(FPS)
        self.played += ms / 1000
        pygame.display.set_caption(
            f"Player's money: {self.player.money}. Player's hp: {self.player.hp} Played: {self.played:.2f}")
        self.player.update(self.up, self.down, self.left, self.right, ms)
        self.coins.update()

        if not self.coins:
            if self.level < len(LEVELS) - 1:
                self.level += 1
            self.load_map()

    def render(self):
        self.display.blit(self.background, (0, 0))
        self.objects.draw(self.display)
        pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()
    pygame.quit()
