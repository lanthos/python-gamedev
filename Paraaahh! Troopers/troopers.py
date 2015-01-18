"""
 Paratrooper class.

"""

import pygame
import random


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

    def __init__(self, image, rect, ground):
        pygame.sprite.Sprite.__init__(self)

        self.image, self.rect = image, rect
        self.image = pygame.transform.scale(self.image, (16, 30))
        self.rect = self.image.get_rect()
        self.ground = ground
        self.speed = 4
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()

        # set states

        self.stopped = 0
        self.falling = 1
        self.chute_attached = False

    def update(self):
        if self.falling:
            if not self.chute_attached:
                if self.rect.bottom + self.speed < self.ground.top:
                    self.rect = self.rect.move((0, self.speed))
                if self.rect.bottom > self.area.centery - 100:
                    random.seed()
                    if random.randint(1, 10) < 3:
                        self.speed = 2
                        self.chute_attached = True
            elif self.chute_attached:
                if self.rect.bottom + self.speed < self.ground.top:
                    self.rect = self.rect.move((0, self.speed))
                    self.para.rect.center = self.rect.midtop
                else:
                    # self.rect.bottom = self.ground.top
                    self.falling = 0
                    self.stopped = 1
        else:
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
        # self.ground = ground

    # def update(self):
    #     if self.attached == 1:
    #         self.rect
    #     else:
    #         self.remove_please = 1

