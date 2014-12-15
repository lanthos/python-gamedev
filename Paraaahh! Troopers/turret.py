'''
Class for the turret station.
'''

import pygame
import math

# Globals constants defined here.
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (187, 8, 0)
BLUE = (5, 61, 244)


class Turret():  # add pygame.sprite.Sprite if going to use sprites.  Maybe.

    def __init__(self, screen):
        # super(turret, self).__init__()
        self.screen = screen
        self.turret_direction = 0
        self.speed = 2
        self.score = 0
        self.hit_counter = 0
        self.hit = False
        self.hit_move = False

    def draw(self):
        self.screen.blit()

    def update(self):
        continue

    def move(self, move_direction):
        if move_direction == 'left':
            self.turret_direction -= 1
            self.angle_rad -= math.pi/8
        if move_direction == 'right':
            self.turret_direction += 1
            self.angle_rad += math.pi/8

    def shoot(self, bullet):
        if bullet.time_alive <= 0:
            bullet.rect.x = self.turret_x
            bullet.rect.y = self.turret_y
            bullet.time_alive = 30
            self.turret_shot.play()
            if bullet.color == 'red':
                bullet.angle_rad = self.angle_rad
            elif bullet.color == 'blue':
                bullet.angle_rad_blue = self.angle_rad_blue

    def been_shot(self):
        if self.hit_counter > 0:
            if self.hit_move:
                self.turret_x -= 50 * round(math.cos(self.angle_rad), 3)
                if self.turret_x < 20:
                    self.turret_x = 660 - self.turret_x
                if self.turret_x > 680:
                    self.turret_x = 20 + (self.turret_x - 680)
                self.turret_y -= 50 * round(math.sin(self.angle_rad), 3)
                if self.turret_y < 100:
                    self.turret_y = 580 - self.turret_y
                if self.turret_y > 580:
                    self.turret_y = 100 + (self.turret_y - 580)
                self.hit_move = False
            self.turret_direction -= 1
            self.angle_rad -= math.pi/8
            self.draw_red()
            self.hit_counter -= 1