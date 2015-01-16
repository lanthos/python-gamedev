'''
Class for the turret station.
'''

import pygame
import math
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


def load_image(name):
    spritesheet = pygame.image.load(name).convert()
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
        self.score = 0
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
        self.bullet = bullet.convert()
        self.rect = self.bullet.get_rect()
        self.speed = 15
        self.movepos = (0, 0)

    def update(self):
        rad = self.direction * (math.pi / 180)
        dx, dy = self.speed * math.cos(rad), -self.speed * math.sin(rad)
        self.rect = self.rect.move((dx, dy))


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


class Helicopter(pygame.sprite.Sprite):

    def __init__(self, image1, image2, rect):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.image1, self.image2, self.rect = image1, image2, rect
        self.images.append(self.image1)
        self.images.append(self.image2)

        self.state = 0
        self.speed = random.randrange(2, 20)
        self.direction = 1
        self.set_image()

    def set_image(self):
        self.image = self.images[self.state]
        if self.state < len(self.images) - 1:
            self.state += 1
        else:
            self.state = 0

    def update(self):
        dx = self.speed * self.direction
        self.rect = self.rect.move((dx, 0))
        self.set_image()

    def flip_images(self):
        new_images = []
        for i in self.images:
            new_images.append(pygame.transform.flip(i, 1, 0))
        self.images = new_images
        self.set_image()


class Plane(pygame.sprite.Sprite):

    def __init__(self, image, rect):
        pygame.sprite.Sprite.__init__(self)

        self.image, self.rect = image, rect


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

