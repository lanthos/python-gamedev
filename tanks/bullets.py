'''
Bullets class for tanks game.  There are color differences in the bullets for the same reason as the tanks.  Please see
tank comments for full reasoning behind that.

Created by Jeremy Kenyon.  For questions contact lanthos@gmail.com.
'''

import pygame
import math


class Bullet(pygame.sprite.Sprite):

    def __init__(self, bullet_color, tank_color, DISPLAYSURF, game_map, enemy_tank, my_tank):
        super(Bullet, self).__init__()
        self.image = pygame.Surface([4, 4])
        self.image.fill(bullet_color)
        self.rect = self.image.get_rect()
        self.game_map = game_map
        self.rect.x = -100
        self.rect.y = -100
        self.tileX = int(self.rect.x / self.game_map.TILESIZE)
        self.tileY = int(self.rect.y / self.game_map.TILESIZE)
        self.previous_x_vector = self.rect.x
        self.previous_y_vector = self.rect.y
        self.x_velocity = 0
        self.y_velocity = 0
        self.shot_type_normal = 0
        self.shot_type_guided = 1
        self.shot_type_bounce = 2
        self.speed = 6
        self.time_alive = 0
        self.color = tank_color
        self.bullet_color = bullet_color
        self.DISPLAYSURF = DISPLAYSURF
        self.enemy_tank = enemy_tank
        self.my_tank = my_tank
        self.tank_hit = pygame.mixer.Sound("tank_hit.wav")

    def check_wall(self):
        self.tileX = int(self.rect.x / self.game_map.TILESIZE)
        self.tileY = int(self.rect.y / self.game_map.TILESIZE)
        try:
            if self.game_map.tilemap[self.tileY][self.tileX] == self.game_map.wall:
                return True
        except IndexError:
            self.rect.x = -100
            self.rect.y = -100
            self.time_alive = 0

    def update(self):
        if self.time_alive > 0:
            if self.color == 'red':
                # angle and speed are passed into the bullets from the tank class when it takes a shot.  The only time
                # here that the angle and speed are calculated is when using guided missiles.
                if self.game_map.shot_type == self.shot_type_normal:
                    self.rect.x += self.x_velocity
                    self.rect.y += self.y_velocity
                    if self.check_wall():
                        self.rect.x = -100
                        self.rect.y = -100
                        self.time_alive = 0
                elif self.game_map.shot_type == self.shot_type_guided:
                    self.rect.x += self.speed * round(math.cos(self.my_tank.angle_rad), 3)
                    self.rect.y += self.speed * round(math.sin(self.my_tank.angle_rad), 3)
                    if self.check_wall():
                        self.rect.x = -100
                        self.rect.y = -100
                        self.time_alive = 0
                elif self.game_map.shot_type == self.shot_type_bounce:
                    previous_x = self.rect.x
                    previous_y = self.rect.y
                    self.rect.x += self.x_velocity
                    self.rect.y += self.y_velocity
                    previous_tile_x = int(previous_x / self.game_map.TILESIZE)
                    previous_tile_y = int(previous_y / self.game_map.TILESIZE)
                    if self.check_wall():
                        # If the bouncing shot hits a wall it checks to see if you were coming horizontally or
                        # vertically and determines the correct axis to bounce based upon that.  If you hit a corner
                        # it will bounce both.
                        both_tests_failed = True
                        if previous_tile_x != self.tileX:
                            if self.game_map.tilemap[self.tileY][previous_tile_x] != self.game_map.wall:
                                self.x_velocity *= -1
                                both_tests_failed = False
                        if previous_tile_y != self.tileY:
                            if self.game_map.tilemap[previous_tile_y][self.tileX] != self.game_map.wall:
                                self.y_velocity *= -1
                                both_tests_failed = False
                        if both_tests_failed:
                            self.x_velocity *= -1
                            self.y_velocity *= -1
                self.time_alive -= 1
                if self.time_alive <= 0:
                    self.rect.x = -100
                    self.rect.y = -100
            if self.color == 'blue':
                if self.game_map.shot_type == self.shot_type_normal:
                    self.rect.x += self.x_velocity
                    self.rect.y -= self.y_velocity
                    if self.check_wall():
                        self.rect.x = -100
                        self.rect.y = -100
                        self.time_alive = 0
                elif self.game_map.shot_type == self.shot_type_guided:
                    self.rect.x += self.speed * round(math.cos(self.my_tank.angle_rad_blue), 3)
                    self.rect.y -= self.speed * round(math.sin(self.my_tank.angle_rad_blue), 3)
                    if self.check_wall():
                        self.rect.x = -100
                        self.rect.y = -100
                        self.time_alive = 0
                elif self.game_map.shot_type == self.shot_type_bounce:
                    previous_x = self.rect.x
                    previous_y = self.rect.y
                    self.rect.x += self.x_velocity
                    self.rect.y -= self.y_velocity
                    previous_tile_x = int(previous_x / self.game_map.TILESIZE)
                    previous_tile_y = int(previous_y / self.game_map.TILESIZE)
                    if self.check_wall():
                        both_tests_failed = True
                        if previous_tile_x != self.tileX:
                            if self.game_map.tilemap[self.tileY][previous_tile_x] != self.game_map.wall:
                                self.x_velocity *= -1
                                both_tests_failed = False
                        if previous_tile_y != self.tileY:
                            if self.game_map.tilemap[previous_tile_y][self.tileX] != self.game_map.wall:
                                self.y_velocity *= -1
                                both_tests_failed = False
                        if both_tests_failed:
                            self.x_velocity *= -1
                            self.y_velocity *= -1
                self.time_alive -= 1
                if self.time_alive <= 0:
                    self.rect.x = -100
                    self.rect.y = -100
        if self.enemy_tank.tank_x - 10 <= self.rect.x <= self.enemy_tank.tank_x + 10 \
                and self.enemy_tank.tank_y - 12 <= self.rect.y <= self.enemy_tank.tank_y + 12:
            self.rect.x = -100
            self.rect.y = -100
            self.time_alive = 0
            self.tank_hit.play()
            self.enemy_tank.hit_counter = 30
            self.enemy_tank.hit = True
            self.enemy_tank.hit_move = True
            self.my_tank.score += 1

    def draw(self):
        self.DISPLAYSURF.blit(self.image, (self.rect.x, self.rect.y))

    def reset(self):
        self.rect.x = -100
        self.rect.y = -100
        self.time_alive = 0