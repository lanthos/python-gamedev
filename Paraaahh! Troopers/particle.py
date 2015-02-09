import random
import pygame
import math


class Particle(pygame.sprite.Sprite):

    def __init__(self, startx, starty, color, object):
        pygame.sprite.Sprite.__init__(self)
        random.seed()
        particle = pygame.Surface((3, 3))
        particle.fill(color)
        self.screen = pygame.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.particle = particle.convert()
        self.rect = self.particle.get_rect()
        self.x_offset = random.randrange(1, 20) + 1
        self.y_offset = random.randrange(-20, 20)
        # self.y_velocity_offset = int(random.random() * 2 + 1)
        # self.x_velocity_offset = int(random.random() * 2 + 1)
        self.rect.x = self.x_offset + startx
        self.rect.y = self.y_offset + starty
        self.color = color
        self.speed = random.randrange(5, 10)
        if object == 'base':
            random.seed()
            self.direction = random.randrange(20, 160)
            self.gravity = 1
            self.x_offset = random.randrange(1, 75) + 1
            self.y_offset = random.randrange(-80, 50) + 1
            self.rect.x = self.x_offset + startx
            self.rect.y = self.y_offset + starty
            # self.speed = 5
        else:
            self.direction = random.randrange(1, 180)
            self.gravity = 2
        # if not shot.rad:
        self.rad = self.direction * (math.pi / 180)
        # else:
        #     self.rad = shot.rad
        self.timer = 15
        self.dx, self.dy = self.speed * math.cos(self.rad), -self.speed * math.sin(self.rad)

    def update(self):
        self.dy += self.gravity
        # dx += self.x_velocity_offset
        self.rect = self.rect.move((self.dx, self.dy))
        self.timer -= 1