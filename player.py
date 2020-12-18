from parents import *
import pygame as pg

class Player(Sprite):
    # variables that arent supposed to be used in other objects
    spikes = None
    coins = None
    medkits = None
    damage = None
    frames = 0

    def __init__(self, x=150, y=150, size=96, speed=10, image=MISSING):
        Sprite.__init__(self, x, y, size, speed, image)
        self.money = 0
        self.hp_max = 100
        self.hp_start = self.hp_max
        self.hp = self.hp_start
        self.image_main = self.image
        self.image_flipped = False
        self.delay = 500
        self.cooldown = self.delay
        self.on_ground = False
        self.speed_y = 0
        self.jump_force = 10
        self.speed_x = 0
        self.accel_x = 2
        self.speed_x_max = 7
        self.x0 = x
        self.y0 = y
        self.tick = 0
        self.frames = 0
        self.animation_speed = 6
        self.taking_damage = False

    # sets position from load_map
    def set_position(self, x, y):
        self.rect.x, self.rect.y = x, y

    def update(self, up, down, left, right, ms):
        # method that checks if object consumes consumables
        self.collide_check(ms)
        print(self.taking_damage)
        # count for animation pick
        self.frames += ms
        if not self.frames % (FPS // self.animation_speed):
            self.tick += 1
        if self.tick + 1 >= len(PLAYER_ASSETS['idle']):
            self.tick = 0

        # whilst player is doing nothing
        if self.on_ground:
            if self.image_flipped:
                self.image = pg.transform.scale(PLAYER_ASSETS_FLIPPED['idle'][self.tick], (self.size, self.size))
            else:
                self.image = pg.transform.scale(PLAYER_ASSETS['idle'][self.tick], (self.size, self.size))
        else:
            self.tick = 0

        # jumping and falling (y movement)
        if up == down:
            pass
        if not self.on_ground:
            self.speed_y += GRAVITY
        else:
            self.speed_y = 0
        if up and self.on_ground and self.rect.top != WIN_SIZE[1]:
            self.speed_y -= self.jump_force
            self.on_ground = False

        self.rect.bottom += self.speed_y

        # collide check - if on block
        is_bottom_colliding = False
        for block in self.solid_blocks:
            if pg.sprite.collide_rect(self, block):
                if self.speed_y < 0:
                    self.rect.top = block.rect.bottom
                    self.speed_y = 0
                else:
                    self.rect.bottom = block.rect.top
                    self.on_ground = True
            if -TILE_SIZE <= self.rect.x - block.rect.x <= TILE_SIZE:
                if block.rect.top == self.rect.bottom:
                    is_bottom_colliding = True

        self.on_ground = is_bottom_colliding

        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > WIN_SIZE[1]:
            self.rect.bottom = WIN_SIZE[1]

        # walking (x movement)
        if left == right:
            self.speed_x *= 0.9
            if abs(self.speed_x) < .5:
                self.speed_x = 0
        elif left:
            self.speed_x -= self.accel_x
            if abs(self.speed_x) > self.speed_x_max:
                self.speed_x = -self.speed_x_max
            self.image = pg.transform.scale(PLAYER_ASSETS_FLIPPED['walk'][self.tick], (self.size, self.size))
            self.image_flipped = True
        elif right:
            self.speed_x += self.accel_x
            if abs(self.speed_x) > self.speed_x_max:
                self.speed_x = self.speed_x_max
            self.image = pg.transform.scale(PLAYER_ASSETS['walk'][self.tick], (self.size, self.size))
            self.image_flipped = False

        self.rect.x += self.speed_x

        # collide check - if touching block
        for block in self.solid_blocks:
            if pg.sprite.collide_rect(self, block):
                if self.speed_x < 0:
                    self.rect.left = block.rect.right
                    self.speed_x = 0
                else:
                    self.rect.right = block.rect.left
                    self.speed_x = 0

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIN_SIZE[0]:
            self.rect.right = WIN_SIZE[0]

        if self.hp <= 0:
            self.respawn()

    def collide_check(self, ms):
        if self.coins:
            for coin in self.coins:
                if pg.sprite.collide_rect(self, coin):
                    self.money += coin.value
                    coin.kill()

        if self.spikes:
            for spike in self.spikes:
                if pg.sprite.collide_rect(self, spike):
                    self.hp -= self.take_damage(ms, spike.damage)

        if self.medkits:
            for medkit in self.medkits:
                if pg.sprite.collide_rect(self, medkit):
                    if self.hp + medkit.value < 100:
                        self.hp += medkit.value
                    else:
                        self.hp = self.maxhp
                    medkit.kill()

    # method that changes player hp depending on colliding spikes or not
    def take_damage(self, ms, damage):
        if self.cooldown > 0:
            self.cooldown -= ms
            self.taking_damage = False
            return 0
        if self.cooldown <= 0:
            self.cooldown = 0
        if self.cooldown == 0:
            self.cooldown = self.delay
            self.taking_damage = True
            return damage

    # method called when player hp <= 0 - death
    def respawn(self):
        self.money = round(self.money * 0.9)
        self.rect.topleft = self.x0, self.y0
        self.hp = self.hp_max
