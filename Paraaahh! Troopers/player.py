'''
Class for the turret station.
'''

import pygame
import math
import random
import os

# Globals constants defined here.
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (5, 61, 244)
GREY = (199, 199, 199)
GREEN = (63, 177, 79)
RED = (187, 8, 0)
YELLOW = (229, 255, 6)


def load_image(name):
    fullname = os.path.join("data", name)
    spritesheet = pygame.image.load(fullname).convert()
    spritesheet.set_colorkey(BLACK)
    spritesheet.convert_alpha()
    return spritesheet, spritesheet.get_rect()


class Turret(pygame.sprite.Sprite):

    def __init__(self, ground):
        # super(Turret, self).__init__()
        pygame.sprite.Sprite.__init__(self)
        self.screen = pygame.display.get_surface()
        self.turret_direction = 90
        self.speed = 2
        self.hit_counter = 0
        self.hit = False
        self.hit_move = False
        # self.bunker = ((self.screen.get_width() / 2) - 75, self.screen.get_height() / 1.22, 144, 70)
        # self.turret = (self.screen.get_width() / 2, int(self.screen.get_height() / 1.2))
        # self.gun = pygame.Rect(self.screen.get_width() / 2 - 5, self.screen.get_height() / 1.4, 10, 70)
        self.base, self.rect = load_image('turret.bmp')

        self.canonbase = pygame.Surface((100, 60))
        self.canonbase.fill(GREY)
        self.canonbase = self.canonbase.convert()
        self.canontop = pygame.Surface((50, 40))
        self.canontop.fill(BLUE)
        self.canontop = self.canontop.convert()

        self.cannonbase_rect = self.canonbase.get_rect()
        self.cannontop_rect = self.canontop.get_rect()
        self.cannonbase_rect.midbottom = ground.midtop
        self.cannontop_rect.midbottom = self.cannonbase_rect.midtop


        self.image = self.base
        self.reinit()

    def reinit(self):
        self.state = "still"
        self.angle = 90
        self.speed = 3
        self.rect.center = self.cannonbase_rect.midtop
        self.rect = self.rect.move((0, -36))

    def update(self):
        rotated = pygame.transform.rotate(self.base, self.angle)
        self.rect = rotated.get_rect()
        self.rect.center = self.cannonbase_rect.midtop
        self.rect = self.rect.move((0, -36))
        self.image = rotated
        if self.state == "clockwise":
            self.move_clockwise()
        elif self.state == "counterclockwise":
            self.move_counter_clockwise()

    def move_clockwise(self):
        if self.angle - self.speed > 25:
            self.angle -= self.speed
            self.state = "clockwise"
        else:
            self.angle = 25
            self.state = "still"

    def move_counter_clockwise(self):
        if self.angle + self.speed < 155:
            self.angle += self.speed
            self.state = "counterclockwise"
        else:
            self.angle = 155
            self.state = "still"

    def halt(self):
        self.state = "still"


class Bullet(pygame.sprite.Sprite):

    def __init__(self):

        #init sprite
        pygame.sprite.Sprite.__init__(self)

        bullet = pygame.Surface((6, 6))
        bullet.fill(YELLOW)
        self.screen = pygame.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.bullet = bullet.convert()
        self.rect = self.bullet.get_rect()
        self.speed = 15
        self.movepos = (0, 0)
        self.test = 0
        self.remove_please = 0

    def update(self):
        if not self.test:
            rad = self.direction * (math.pi / 180)
            dx, dy = self.speed * math.cos(rad), -self.speed * math.sin(rad)
            self.rect = self.rect.move((dx, dy))
        if self.rect.bottom < self.screen_rect.top:
            self.remove_please = 1