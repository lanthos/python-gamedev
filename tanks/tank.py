'''
Tank Class for the tanks game.  There are two different tank colors here which impact how they are treated.  This has to
do with the blue tanks using a single image that is rotated and the red tanks using a sprite sheet with every angle in
it.  The Pygame image rotate function can only take degrees and everything else is done in radians which is why there
are two colors and they are handled differently like this.

Created by Jeremy Kenyon.  For questions contact lanthos@gmail.com.
'''

import pygame
import math
import os
import pyglet

# Globals constants defined here.
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (187, 8, 0)
BLUE = (5, 61, 244)


class Tank():
    '''
    I added a lot of stuff in init that doesn't get used immediately.  I added it because I was getting warnings about
    assigning things to self. outside of init when I tried to do it in other functions so figured this was best practice
    but I could be wrong. :)

    I passed along things in the init to add them to the class for easy access instead of doing it per function, e. g.
    game_map, the different tanks, so that there would be less typing to do over all.  Not sure if this is best practice
    but it worked well for what I was trying to do.
    '''
    def __init__(self, tank_x, tank_y, color):
        # super(Tank, self).__init__()
        self.tank_x = tank_x
        self.tank_y = tank_y
        self.tileX = None
        self.tileY = None
        self.DISPLAYSURF = None
        self.enemy_tank = None
        self.tank_direction = 0
        self.speed = 2
        self.score = 0
        self.color = color
        self.hit_counter = 0
        self.hit = False
        self.hit_move = False
        self.tank_shot = pyglet.media.load(os.path.join('data', 'tank_shot.wav'), streaming=False)

    def hack(self, color):
        # This was a hack that was needed so that I could initialize the tanks before a color was selected so that the
        # map class could have copies of the tank objects for state loading.
        if color == 'red':
            self.angle_rad = 0
            self.spritesheet = pygame.image.load(os.path.join('data', 'red_tanks.bmp')).convert()
            self.tanks = []
            for nbr in range(8):
                self.tanks.append(self.spritesheet.subsurface((40*nbr), 0, 40, 40))
            for nbr in range(8):
                self.tanks.append(self.spritesheet.subsurface((40*nbr), 40, 40, 40))
            for nbr in range(len(self.tanks)):
                self.tanks[nbr].set_colorkey(WHITE)
                self.tanks[nbr] = self.tanks[nbr].convert_alpha()
        if color == 'blue':
            self.angle_deg = 180
            self.angle_rad_blue = math.pi
            self.spritesheet = pygame.image.load(os.path.join('data', 'blue_tank.bmp')).convert()
            self.spritesheet.set_colorkey(WHITE)
            self.spritesheet.convert_alpha()

    def draw_red(self):
        self.DISPLAYSURF.blit(self.tanks[self.tank_direction % 16],
                              (self.tank_x - self.tanks[self.tank_direction % 16].get_width() / 2,
                               self.tank_y - self.tanks[self.tank_direction % 16].get_height() / 2))

    def draw_blue(self):
        self.rotated_image = pygame.transform.rotate(self.spritesheet, self.angle_deg)
        self.DISPLAYSURF.blit(pygame.transform.rotate(self.spritesheet, self.angle_deg),
                              (self.tank_x - self.rotated_image.get_width() / 2, self.tank_y -
                               self.rotated_image.get_height() / 2))

    def check_wall(self):
        # self.game_map is assigned outside of the class.  I know I know, it's bad but it's the only way I could
        # figure out how to make state saving work with tanks and the map.
        for i in range(0, 11):
            self.tileX = int((self.tank_x + i) / self.game_map.TILESIZE)
            self.tileY = int((self.tank_y + i) / self.game_map.TILESIZE)
            if self.game_map.tilemap[self.tileY][self.tileX] == self.game_map.wall:
                return True
        for i in range(0, 11):
            self.tileX = int((self.tank_x - i) / self.game_map.TILESIZE)
            self.tileY = int((self.tank_y - i) / self.game_map.TILESIZE)
            if self.game_map.tilemap[self.tileY][self.tileX] == self.game_map.wall:
                return True

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
                self.tileX = int(self.tank_x / self.game_map.TILESIZE)
                self.tileY = int(self.tank_y / self.game_map.TILESIZE)
                deltaX = self.tank_x - self.enemy_tank.tank_x
                deltaY = self.tank_y - self.enemy_tank.tank_y
                dist = math.sqrt(deltaX * deltaX + deltaY * deltaY)
                if self.check_wall() or dist < 25:
                    self.tank_x -= (self.speed - 20) * round(math.cos(self.angle_rad), 3) * -1
                    self.tank_y -= (self.speed - 20) * round(math.sin(self.angle_rad), 3) * -1
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
                self.tileX = int(self.tank_x / self.game_map.TILESIZE)
                self.tileY = int(self.tank_y / self.game_map.TILESIZE)
                deltaX = self.tank_x - self.enemy_tank.tank_x
                deltaY = self.tank_y - self.enemy_tank.tank_y
                dist = math.sqrt(deltaX * deltaX + deltaY * deltaY)
                if self.check_wall() or dist < 25:
                    self.tank_x -= (self.speed - 20) * round(math.cos(self.angle_rad_blue), 3) * -1
                    self.tank_y -= (self.speed - 20) * round(math.sin(self.angle_rad_blue), 3) * 1

    def shoot(self, bullet):
        if bullet.time_alive <= 0:
            # Here we set the location of the bullet to be at the location of the tank.
            bullet.rect.x = self.tank_x
            bullet.rect.y = self.tank_y
            bullet.time_alive = 30
            self.tank_shot.play()
            # and here we set the initial velocity for the bullets so we don't do a lot of calculations in the bullet
            # class itself and cause confusion.  It's not fun, let me tell you.
            if bullet.color == 'red':
                bullet.angle_rad = self.angle_rad
                bullet.x_velocity = bullet.speed * round(math.cos(bullet.angle_rad), 3)
                bullet.y_velocity = bullet.speed * round(math.sin(bullet.angle_rad), 3)
            elif bullet.color == 'blue':
                bullet.angle_rad_blue = self.angle_rad_blue
                bullet.x_velocity = bullet.speed * round(math.cos(bullet.my_tank.angle_rad_blue), 3)
                bullet.y_velocity = bullet.speed * round(math.sin(bullet.my_tank.angle_rad_blue), 3)

    def been_shot(self, color, bullet):
        '''
        This function makes sure that if the tanks are at the corners of the map when shot that they get wrapped around
        to the other side.  They also spin the tank around when it gets shot.
        '''
        if color == 'red':
            if self.hit_counter > 0:
                bullet.reset()
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
                bullet.reset()
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
        if self.hit_counter <= 0:
            self.hit = False


def degree_to_radian(degree):
    return degree * math.pi/180