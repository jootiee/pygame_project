from config import * 
import pygame as pg

class Menu():
    def __init__(self):
        pg.init()
        self.state = 0
        self.display = pg.display.set_mode(WIN_SIZE)
        self.background = MENU[self.state]
        self.background = pg.transform.scale(self.background, WIN_SIZE)
        self.clock = pg.time.Clock()
        self.down = self.up = self.choice = False
        self.running = True

    def update(self):
        ms = self.clock.tick(FPS)

        if self.down:
            self.state += 1
        if self.up:
            self.state -= 1
        
        if self.state < 0:
            self.state = 0
        if self.state > len(MENU) - 1:
            self.state = len(MENU) - 1
        
        self.background = MENU[self.state]
        self.background = pg.transform.scale(self.background, WIN_SIZE)

        if self.choice:
            if self.state == 0:
                return 'play'
            if self.state == 1:
                pass
            if self.state == 2:
                return 'exit'
        
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
                if event.key == pg.K_r:
                    self.restart = True
                if event.key == pg.K_SPACE:
                    self.choice = True
            if event.type == pg.KEYUP:
                if event.key == pg.K_s:
                    self.down = False
                if event.key == pg.K_w:
                    self.up = False
                if event.key == pg.K_SPACE:
                    self.choice = False
                if event.key == pg.K_ESCAPE:
                    self.running = False
    
    def render(self):
        self.display.blit(self.background, (0, 0))
        pg.display.update()

    def run(self):
        while self.running:
            self.render()
            result = self.update()
            if result == 'exit':
                return 'exit'
            elif result == 'play':
                return 'play'