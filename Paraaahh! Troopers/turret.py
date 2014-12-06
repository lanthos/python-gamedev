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
        # super(Tank, self).__init__()
        self.screen = screen
        self.tank_direction = 0
        self.speed = 2
        self.score = 0
        self.color = color
        self.hit_counter = 0
        self.hit = False
        self.hit_move = False

    def draw(self):
        self.screen.blit()

    def update(self, game_map, tank, color):
        if color == 'red':
            self.tileX = int(self.tank_x / game_map.TILESIZE)
            self.tileY = int(self.tank_y / game_map.TILESIZE)
            if game_map.tilemap[self.tileY][self.tileX] == game_map.wall or tank.tileX == self.tileX \
                    and tank.tileY == self.tileY:
                self.tank_x -= (self.speed - 20) * round(math.cos(self.angle_rad), 3) * -1
                self.tank_y -= (self.speed - 20) * round(math.sin(self.angle_rad), 3) * -1
            self.been_shot('red')
        elif color == 'blue':
            self.tileX = int(self.tank_x / game_map.TILESIZE)
            self.tileY = int(self.tank_y / game_map.TILESIZE)
            if game_map.tilemap[self.tileY][self.tileX] == game_map.wall or tank.tileX == self.tileX \
                    and tank.tileY == self.tileY:
                self.tank_x -= (self.speed - 20) * round(math.cos(self.angle_rad_blue), 3) * -1
                self.tank_y -= (self.speed - 20) * round(math.sin(self.angle_rad_blue), 3) * 1
            self.been_shot('blue')
        if self.hit_counter <= 0:
            self.hit = False

    def move(self, move_direction, color):
        if color == 'red':
            if move_direction == 'left':
                self.tank_direction -= 1
                self.angle_rad -= math.pi/8
                self.draw_red()
            if move_direction == 'right':
                self.tank_direction += 1
                self.angle_rad += math.pi/8
                self.draw_red()
            if move_direction == 'forward':
                self.tank_x += self.speed * round(math.cos(self.angle_rad), 3)
                self.tank_y += self.speed * round(math.sin(self.angle_rad), 3)
                print 'red tank_x: %s, red tank_y: %s, tilex: %s, tiley: %s' % (self.tank_x, self.tank_y, self.tileX, self.tileY)
                print 'angle_rad: %s' % self.angle_rad
        if color == 'blue':
            if move_direction == 'left':
                self.angle_deg += 22.5
                self.angle_rad_blue = degree_to_radian(self.angle_deg)
                self.draw_blue()
            if move_direction == 'right':
                self.angle_deg -= 22.5
                self.angle_rad_blue = degree_to_radian(self.angle_deg)
                self.draw_blue()
            if move_direction == 'forward':
                self.tank_x += self.speed * round(math.cos(self.angle_rad_blue), 3)
                self.tank_y -= self.speed * round(math.sin(self.angle_rad_blue), 3)
                print 'blue tank_x: %s, blue tank_y: %s, blue angle_rad: %s' % (self.tank_x, self.tank_y, self.angle_rad_blue)

    def shoot(self, bullet):
        if bullet.time_alive <= 0:
            bullet.rect.x = self.tank_x
            bullet.rect.y = self.tank_y
            bullet.time_alive = 30
            self.tank_shot.play()
            if bullet.color == 'red':
                bullet.angle_rad = self.angle_rad
            elif bullet.color == 'blue':
                bullet.angle_rad_blue = self.angle_rad_blue

    def been_shot(self, color):
        if color == 'red':
            if self.hit_counter > 0:
                if self.hit_move:
                    self.tank_x -= 50 * round(math.cos(self.angle_rad), 3)
                    if self.tank_x < 20:
                        self.tank_x = 660 - self.tank_x
                    if self.tank_x > 680:
                        self.tank_x = 20 + (self.tank_x - 680)
                    self.tank_y -= 50 * round(math.sin(self.angle_rad), 3)
                    if self.tank_y < 100:
                        self.tank_y = 580 - self.tank_y
                    if self.tank_y > 580:
                        self.tank_y = 100 + (self.tank_y - 580)
                    self.hit_move = False
                self.tank_direction -= 1
                self.angle_rad -= math.pi/8
                self.draw_red()
                self.hit_counter -= 1
        if color == 'blue':
            if self.hit_counter > 0:
                if self.hit_move:
                    self.tank_x -= 50 * round(math.cos(self.angle_rad_blue), 3)
                    if self.tank_x < 20:
                        self.tank_x = 660 - self.tank_x
                    if self.tank_x > 680:
                        self.tank_x = 20 + (self.tank_x - 680)
                    self.tank_y -= 50 * round(math.sin(self.angle_rad_blue), 3)
                    if self.tank_y < 100:
                        self.tank_y = 580 - self.tank_y
                    if self.tank_y > 580:
                        self.tank_y = 100 + (self.tank_y - 580)
                    self.hit_move = False
                self.angle_deg += 22.5
                self.angle_rad_blue = degree_to_radian(self.angle_deg)
                self.draw_blue()
                self.hit_counter -= 1

def degree_to_radian(degree):
    return degree * math.pi/180