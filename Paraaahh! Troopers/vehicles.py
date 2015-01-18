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

    def __init__(self, image1, image2, rect):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.image1, self.image2, self.rect = image1, image2, rect
        self.images.append(self.image1)
        self.images.append(self.image2)

        self.state = 0
        self.speed = random.randrange(5, 15)
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