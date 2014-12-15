'''
Bullets class for tanks game.
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
        self.previous_tileX = self.tileX
        self.previous_tileY = self.tileY
        self.previous_x_vector = self.rect.x
        self.previous_y_vector = self.rect.y
        self.speed = 6
        self.time_alive = 0
        self.color = tank_color
        self.bullet_color = bullet_color
        self.DISPLAYSURF = DISPLAYSURF
        self.enemy_tank = enemy_tank
        self.my_tank = my_tank
        self.bounce_x = False
        self.bounce_y = False
        self.tank_hit = pygame.mixer.Sound("tank_hit.wav")

    def check_wall(self):
        for i in range(0, 5):
            self.tileX = int(round((self.rect.x + i) / self.game_map.TILESIZE))
            self.tileY = int(round((self.rect.y + i) / self.game_map.TILESIZE))
            try:
                if self.game_map.tilemap[self.tileY][self.tileX] == self.game_map.wall:
                    return True
            except IndexError:
                self.rect.x = -100
                self.rect.y = -100
                self.time_alive = 0
        for i in range(0, 5):
            self.tileX = int(round((self.rect.x - i) / self.game_map.TILESIZE))
            self.tileY = int(round((self.rect.y - i) / self.game_map.TILESIZE))
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
                if self.game_map.shot_type == 0:
                    self.rect.x += self.speed * round(math.cos(self.angle_rad), 3)
                    self.rect.y += self.speed * round(math.sin(self.angle_rad), 3)
                elif self.game_map.shot_type == 1:
                    self.rect.x += self.speed * round(math.cos(self.my_tank.angle_rad), 3)
                    self.rect.y += self.speed * round(math.sin(self.my_tank.angle_rad), 3)
                elif self.game_map.shot_type == 2:
                    if self.bounce_x:
                        self.rect.x -= self.previous_x_vector
                        if self.check_wall():
                            self.rect.x -= self.previous_x_vector
                        self.previous_x_vector = (self.speed * -1) * round(math.cos(self.angle_rad), 3)
                        self.rect.x += self.previous_x_vector
                    else:
                        self.previous_x_vector = self.speed * round(math.cos(self.angle_rad), 3)
                        self.rect.x += self.previous_x_vector
                    if self.bounce_y:
                        self.rect.y -= self.previous_y_vector
                        if self.check_wall():
                            self.rect.y -= self.previous_y_vector
                        self.previous_y_vector = (self.speed * -1) * round(math.sin(self.angle_rad), 3)
                        self.rect.y += self.previous_y_vector
                    else:
                        self.previous_y_vector = self.speed * round(math.sin(self.angle_rad), 3)
                        self.rect.y += self.previous_y_vector
                self.time_alive -= 1
                #print 'bullet X and Y and angle: %s, %s, %s' % (self.rect.x, self.rect.y, self.angle_rad)
                #print 'cos and sin: %s, %s' % (round(math.cos(self.my_tank.angle_rad), 3), round(math.sin(self.my_tank.angle_rad), 3))
                #print 'current X, Y: {}, {} and previous X, Y: {}, {}'.format(self.tileX, self.tileY, self.previous_tileX, self.previous_tileY)
                if self.time_alive <= 0:
                    self.rect.x = -100
                    self.rect.y = -100
                    #print 'bullets reset'
            if self.color == 'blue':
                if self.bounce_x:
                    self.rect.x += (self.speed * -1) * round(math.cos(self.my_tank.angle_rad_blue), 3)
                else:
                    self.rect.x += self.speed * round(math.cos(self.my_tank.angle_rad_blue), 3)
                if self.bounce_y:
                    self.rect.y -= (self.speed * -1) * round(math.sin(self.my_tank.angle_rad_blue), 3)
                else:
                    self.rect.y -= self.speed * round(math.sin(self.my_tank.angle_rad_blue), 3)
                self.time_alive -= 1
                #print 'bullet X and Y: %s, %s' % (self.rect.x, self.rect.y)
                if self.time_alive <= 0:
                    self.rect.x = -100
                    self.rect.y = -100
                    #print 'bullets reset'
        tempx = int(round(self.rect.x / self.game_map.TILESIZE))
        if tempx != self.previous_tileX:
            self.previous_tileX = self.tileX
            self.tileX = tempx
        tempy = int(round(self.rect.y / self.game_map.TILESIZE))
        if tempy != self.previous_tileY:
            self.previous_tileY = self.tileY
            self.tileY = tempy
        if self.game_map.shot_type == 2:
            # if self.rect.x >= 676 or self.rect.x <= 23 and self.time_alive > 0:
            if self.check_wall() and self.time_alive > 0:
                if self.previous_tileY == self.tileY:
                    if self.bounce_x:
                        self.bounce_x = False
                    else:
                        self.bounce_x = True
                    #print 'bounced x'
            # if self.rect.y <= 102 or self.rect.y >= 575 and self.time_alive > 0:
                elif self.previous_tileX == self.tileX:
                    if self.bounce_y:
                        self.bounce_y = False
                    else:
                        self.bounce_y = True
                    #print 'bounced y'
            if self.time_alive <= 0:
                self.bounce_y = False
                self.bounce_x = False
        else:
            if self.check_wall():
                self.rect.x = -100
                self.rect.y = -100
                self.time_alive = 0
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