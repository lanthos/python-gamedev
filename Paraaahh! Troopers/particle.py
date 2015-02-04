import random
import pygame
import math


class Particle(pygame.sprite.Sprite):

    def __init__(self, startx, starty, color, shot):
        pygame.sprite.Sprite.__init__(self)
        random.seed()
        particle = pygame.Surface((3, 3))
        particle.fill(color)
        self.screen = pygame.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.particle = particle.convert()
        self.rect = self.particle.get_rect()
        self.x_offset = random.randrange(1, 40) + 1
        self.y_offset = random.randrange(1, 40) + 1
        self.y_velocity_offset = int(random.random() * 2 + 1)
        self.x_velocity_offset = int(random.random() * 2 + 1)
        self.rect.x = self.x_offset + startx
        self.rect.y = self.y_offset + starty
        self.color = color
        self.speed = shot.speed / 3 + self.y_velocity_offset
        self.gravity = 12
        self.direction = random.randint(1, 180)
        # if not shot.rad:
        self.rad = self.direction * (math.pi / 180)
        # else:
        #     self.rad = shot.rad
        self.timer = 20
        self.direction = shot.direction

    def update(self):
        dx, dy = self.speed * math.cos(self.rad), -self.speed * math.sin(self.rad)
        dy += self.gravity
        dx *= self.x_velocity_offset
        self.rect = self.rect.move((dx, dy))
        self.timer -= 1