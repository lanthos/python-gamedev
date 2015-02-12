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
        self.base, self.rect = load_image('turret.bmp')

        self.canonbase = pygame.Surface((100, 60))
        self.canonbase.fill(GREY)
        self.canonbase = self.canonbase.convert()
        self.canontop = pygame.Surface((50, 40))
        self.canontop.fill(BLUE)
        self.canontop = self.canontop.convert()

        self.canonbase_rect = self.canonbase.get_rect()
        self.cannontop_rect = self.canontop.get_rect()
        self.canonbase_rect.midbottom = ground.midtop
        self.cannontop_rect.midbottom = self.canonbase_rect.midtop


        self.image = self.base
        self.reinit()

    def reinit(self):
        self.state = "still"
        self.angle = 90
        self.speed = 3
        self.rect.center = self.canonbase_rect.midtop
        self.rect = self.rect.move((0, -36))

    def update(self):
        rotated = pygame.transform.rotate(self.base, self.angle)
        self.rect = rotated.get_rect()
        self.rect.center = self.canonbase_rect.midtop
        self.rect = self.rect.move((0, -36))
        self.image = rotated
        if self.state == "clockwise":
            self.move_clockwise()
        elif self.state == "counterclockwise":
            self.move_counter_clockwise()

    def move_clockwise(self):
        if self.angle - self.speed > 20:
            self.angle -= self.speed
            self.state = "clockwise"
        else:
            self.angle = 20
            self.state = "still"

    def move_counter_clockwise(self):
        if self.angle + self.speed < 160:
            self.angle += self.speed
            self.state = "counterclockwise"
        else:
            self.angle = 160
            self.state = "still"

    def halt(self):
        self.state = "still"


class Bullet(pygame.sprite.Sprite):

    def __init__(self, type):

        #init sprite
        pygame.sprite.Sprite.__init__(self)
        if type == 'bullet':
            bullet = pygame.Surface((6, 6))
            bullet.fill(YELLOW)
        if type == 'mine':
            bullet = pygame.Surface((8, 6))
            bullet.fill(BLUE)
        self.screen = pygame.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.bullet = bullet.convert()
        self.rect = self.bullet.get_rect()
        self.speed = 15
        self.movepos = (0, 0)
        self.test = 0
        self.remove_please = 0
        self.rad = None

    def update(self):
        if not self.test:
            self.rad = self.direction * (math.pi / 180)
            dx, dy = self.speed * math.cos(self.rad), -self.speed * math.sin(self.rad)
            self.rect = self.rect.move((dx, dy))
        if self.rect.bottom < self.screen_rect.top:
            self.remove_please = 1


class Dude(pygame.sprite.Sprite):

    def __init__(self, image1, image2, image3, image4, rect, ground, screen):
        pygame.sprite.Sprite.__init__(self)
        self.imagesa = []
        self.imagesb = []
        self.image1, self.image2, self.image3, self.image4, self.rect = image1, image2, image3, image4, rect
        self.rect = self.image1.get_rect()
        self.imagesa.append(self.image1)
        self.imagesa.append(self.image2)
        self.imagesb.append(self.image3)
        self.imagesb.append(self.image4)
        self.screen = screen
        self.area = self.screen.get_rect()
        self.ground = ground
        self.speed = -3
        self.music = None
        self.state = 0
        self.walking = True
        self.glasses = False
        self.glasses_counter = 10
        self.walk_timer = 3
        self.set_image()
        self.music_playing = False

    def set_image(self):
        if self.walking:
            self.image = self.imagesa[self.state]
            self.walk_timer -= 1
            if self.walk_timer <= 0:
                if self.state < len(self.imagesa) - 1:
                    self.state += 1
                    self.walk_timer = 3
                else:
                    self.state = 0
                    self.walk_timer = 3
        # elif self.glasses:
        #     self.image = self.imagesb[self.state]
        #     if self.state < len(self.imagesb) - 1:
        #         self.state += 1
        #     else:
        #         self.state = 0

    def update(self):
        if self.rect.right + self.speed > self.area.centerx + 70:
            self.rect = self.rect.move((self.speed, 0))
            self.set_image()
        else:
            self.rect.right = self.area.centerx + 70
            self.walking = False
            self.glasses = True
            self.state = 0
        if self.glasses:
            self.image = self.imagesb[0]
            self.glasses_counter -= 1
            if not self.music_playing:
                    self.music.play()
                    self.music_playing = True
            if self.glasses_counter <= 0:
                self.image = self.imagesb[1]
                self.glasses = False