"""
 Paratrooper class.

"""

import pygame
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


class Trooper(pygame.sprite.Sprite):

    def __init__(self, image1, image2, rect, ground, canon, screen):
        pygame.sprite.Sprite.__init__(self)

        self.images = []
        self.image1, self.image2, self.rect = image1, image2, rect
        self.images.append(self.image1)
        self.images.append(self.image2)
        self.image = self.images[1]
        self.rect = self.image1.get_rect()
        self.ground = ground
        self.speed = 4
        self.screen = screen
        self.area = self.screen.get_rect()
        self.canon = canon
        self.winner = 0
        self.number = 0
        self.climbing = 0
        self.sound = None
        self.walking = 0
        self.in_pyramid = 0

        # set states
        self.stopped = 0
        self.falling = 1
        self.chute_attached = False
        self.chute_shot = False

    def update(self):
        # print self.number
        if self.falling:
            if self.chute_shot:
                self.aahh.rect.midbottom = self.rect.midtop
            if not self.chute_attached:
                self.image = self.images[1]
                if self.rect.bottom + self.speed - 1 < self.ground.top:
                    self.rect = self.rect.move((0, self.speed))
                else:
                    self.falling = 0
                    self.stopped = 1
                if not self.chute_shot:
                    if self.rect.bottom > self.area.centery - 100:
                        random.seed()
                        if random.randint(1, 10) < 3:
                            self.speed = 2
                            self.chute_attached = True
            elif self.chute_attached:
                self.image = self.images[0]
                if self.rect.bottom + self.speed < self.ground.top:
                    self.rect = self.rect.move((0, self.speed))
                    self.para.rect.center = self.rect.midtop
                else:
                    # self.rect.bottom = self.ground.top
                    self.falling = 0
                    self.stopped = 1
        else:
            self.falling = 0
            self.image = self.images[0]
            if not self.climbing:
                self.rect.bottom = self.ground.top
            self.para.remove_please = 1


class Parachute(pygame.sprite.Sprite):

    def __init__(self, image, rect):
        pygame.sprite.Sprite.__init__(self)

        self.image, self.rect = image, rect
        self.speed = 2
        self.remove_please = 0
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()

        self.rect = self.image.get_rect()  # makes sure each chute gets its own rect


class Aahh(pygame.sprite.Sprite):

    def __init__(self, image, rect):
        pygame.sprite.Sprite.__init__(self)

        self.image, self.rect = image, rect
        self.rect = self.image.get_rect()
        self.remove_please = 0