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


class Helicopter(pygame.sprite.Sprite):

    def __init__(self, image1a, image2a, image1b, image2b, rect):
        pygame.sprite.Sprite.__init__(self)
        self.imagesa = []
        self.imagesb = []
        self.image1a, self.image2a, self.image1b, self.image2b, self.rect = image1a, image2a, image1b, image2b, rect
        self.imagesa.append(self.image1a)
        self.imagesa.append(self.image2a)
        self.imagesb.append(self.image1b)
        self.imagesb.append(self.image2b)

        self.state = 0
        self.speed = random.randrange(5, 13)
        self.trooper = True
        self.trooper_chance = 60
        self.direction = 1
        self.set_image()
        random.seed()
        self.random_x = random.randint(520, 800)

    def set_image(self):
        if self.trooper:
            self.image = self.imagesa[self.state]
            if self.state < len(self.imagesa) - 1:
                self.state += 1
            else:
                self.state = 0
        else:
            self.image = self.imagesb[self.state]
            if self.state < len(self.imagesb) - 1:
                self.state += 1
            else:
                self.state = 0

    def update(self):
        dx = self.speed * self.direction
        self.rect = self.rect.move((dx, 0))
        self.set_image()

    def flip_images(self):
        new_images = []
        for i in self.imagesa:
            new_images.append(pygame.transform.flip(i, 1, 0))
        self.imagesa = new_images
        new_images = []
        for i in self.imagesb:
            new_images.append(pygame.transform.flip(i, 1, 0))
        self.imagesb = new_images
        self.set_image()


class Plane(pygame.sprite.Sprite):

    def __init__(self, image, rect):
        pygame.sprite.Sprite.__init__(self)

        self.image, self.rect = image, rect

        self.state = 0
        self.speed = random.randrange(5, 13)
        self.direction = 1
        random.seed()
        self.random_x = random.randint(40, 250)
        self.bomb_released = False

    def update(self):
        dx = self.speed * self.direction
        self.rect = self.rect.move((dx, 0))

    def flip_images(self):
        self.image = pygame.transform.flip(self.image, 1, 0)


class Bomb(pygame.sprite.Sprite):

    def __init__(self, image, rect):

        #init sprite
        pygame.sprite.Sprite.__init__(self)

        self.image, self.rect = image, rect
        self.rect = self.image.get_rect()
        # self.screen = pygame.display.get_surface()
        # self.screen_rect = self.screen.get_rect()
        self.speed = random.randint(5, 10)
        # self.movepos = (0, 0)
        self.rad = None
        # self.dx, self.dy = self.speed * math.cos(self.rad), -self.speed * math.sin(self.rad)

    def update(self):
        self.rect = self.rect.move((self.dx, self.dy))