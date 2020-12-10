import pygame
import random
import os
import math

# импорт констант + загрузка ассетов
from config import *

# родительский класс, от которого наследуются остальные


class Sprite(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0, size=100, speed=0, image=PLAYER_ASSETS['idle']):
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


class Spike(Sprite):
    def __init__(self, x=0, y=0, size=100, damage=10, speed=10, image=PLAYER_ASSETS['idle'][0]):
        if x == None:
            x = random.randint(0, WIN_SIZE[0] - size)
        if y == None:
            y = random.randint(0, WIN_SIZE[1] - size)
        Sprite.__init__(self, x, y, size, speed, image)
        self.damage = damage


class Medkit(Sprite):
    def __init__(self, x=None, y=None, size=50, speed=0, image=MEDKIT):
        if x == None:
            x = random.randint(0, WIN_SIZE[0] - size)
        if y == None:
            y = random.randint(0, WIN_SIZE[1] - size)
        Sprite.__init__(self, x, y, size, speed, image)
        self.value = 50


class Coin(Sprite):
    def __init__(self, x=None, y=None, value=5, size=50, speed=10, image=COINS[0]):
        if x is None:
            self.x = random.randint(0, WIN_SIZE[0] - size)
        else:
            self.x = x
        if y is None:
            self.y = random.randint(0, WIN_SIZE[1] - size)
        else:
            self.y = y
        super().__init__(self.x, self.y, size, speed, image)
        self.ticks = random.choice(range(0, 360, 5))
        self.forward = 1
        self.spawn = self.rect.topleft
        self.value = value

    def update(self, *args):
        if self.ticks >= 360:
            self.ticks -= 360
        self.ticks += 5

        if not self.speed:
            return

        dy = math.sin(math.radians(self.ticks)) * self.speed
        self.rect.y = self.spawn[1] + dy


class Player(Sprite):
    spikes = None
    coins = None
    medkits = None
    damage = None

    def __init__(self, x=0, y=0, size=TILE_SIZE, speed=10, image=PLAYER_ASSETS['idle']):
        Sprite.__init__(self, x, y, size, speed, image)
        self.money = 0
        self.hp_max = 100
        self.hp_start = self.hp_max
        self.hp = self.hp_start
        self.x = x
        self.y = y
        self.x0 = self.x
        self.y0 = self.y
        Sprite.__init__(self, self.x, self.y, size, speed, image)
        self.image_main = self.image
        self.image_flipped = pygame.transform.flip(self.image, True, False)
        self.delay = 500
        self.cooldown = self.delay
        self.on_ground = False
        self.speed_y = 0
        self.jump_force = 10
        self.speed_x = 0


    def update(self, up, down, left, right, ms):
        if self.rect.bottom == WIN_SIZE[1]:
            self.on_ground = True
        else:
            self.on_ground = False

        if not self.on_ground:
            self.speed_y += GRAVITY
        else:
            self.speed_y = 0

        if up == down:
            pass
        elif up:
            if self.on_ground:
                self.speed_y = -self.jump_force 

        self.rect.bottom += self.speed_y

        for block in self.solid_blocks:
            if pygame.sprite.collide_rect(self, block):
                if self.speed_y < 0:
                    self.rect.top = block.rect.bottom
                else:
                    self.rect.bottom = block.rect.top
                    self.on_ground = True



        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > WIN_SIZE[1]:
            self.rect.bottom = WIN_SIZE[1]

        if left == right:
            self.speed_x = 0
        elif left:
            self.speed_x = -self.speed
            self.image = self.image_flipped
        else:
            self.speed_x = +self.speed
            self.image = self.image_main
        
        self.rect.x += self.speed_x

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIN_SIZE[0]:
            self.rect.right = WIN_SIZE[0]
        
        self.collide_check(ms)

        if self.hp <= 0:
            self.respawn()

    def collide_check(self, ms):
        if self.coins:
            for coin in self.coins:
                if pygame.sprite.collide_rect(self, coin):
                    self.money += coin.value
                    coin.kill()
        else:
            return True

        if self.spikes:
            for spike in self.spikes:
                if pygame.sprite.collide_rect(self, spike):
                    self.hp -= self.take_damage(ms, spike.damage)

        if self.medkits:
            for medkit in self.medkits:
                if pygame.sprite.collide_rect(self, medkit):
                    if self.hp + medkit.value < 100:
                        self.hp += medkit.value
                    else:
                        self.hp = self.maxhp
                    medkit.kill()


    def take_damage(self, ms, damage):
        if self.cooldown > 0:
            self.cooldown -= ms
            return 0
        if self.cooldown <= 0:
            self.cooldown = 0
        if self.cooldown == 0:
            self.cooldown = self.delay
            return damage

    def respawn(self):
        self.money = round(self.money * 0.9)
        self.rect.topleft = (self.x0, self.y0)
        self.hp = self.hp_max


class Game:
    def __init__(self):
        pygame.init()
        self.display = pygame.display.set_mode(WIN_SIZE)
        pygame.display.set_caption('Вторые шаги котика')
        self.clock = pygame.time.Clock()
        self.running = True
        self.down = self.up = self.left = self.right = False
        self.objects = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.spikes = pygame.sprite.Group()
        self.medkits = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        Player.coins = self.coins
        Player.spikes = self.spikes
        Player.medkits = self.medkits
        Player.solid_blocks = self.solid_blocks
        self.solid_blocks = pygame.sprite.Group()
        self.load_map()
        # for _ in range(random.randint(1, 25)):
        #     Coin().add(self.coins, self.objects)
        # for _ in range(random.randint(1, 15)):
        #     Spike().add(self.spikes, self.objects)
        # for _ in range(random.randint(1, 10)):
        #     Medkit().add(self.medkits, self.objects)
        spike = Spike(image=SPIKE)
        self.player = Player()
        self.player.add(self.objects)
        self.played = 0.0
        self.coins_collected = False
        self.endgame_timecode = None
        self.countdown = False

    def load_map(self):
        map_path = LEVELS[0]
        with open(map_path, encoding='utf-8') as file:
            for y, line in enumerate(file):
                for x, letter in enumerate(line):
                    if letter in MAP.keys():
                        pos = x * TILE_SIZE, y * TILE_SIZE
                        image = MAP[letter]
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
        if self.player.update(self.up, self.down, self.left, self.right, ms) and not self.countdown:
            self.countdown = 5.0
        if self.countdown:
            self.countdown -= ms / 1000
            if self.countdown <= 0:
                self.running = False
        self.coins.update()

    def render(self):
        self.display.fill(BG_COLOR)
        self.objects.draw(self.display)
        pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()
    pygame.quit()
