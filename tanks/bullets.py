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
        self.speed = 6
        self.time_alive = 0
        self.color = tank_color
        self.bullet_color = bullet_color
        self.DISPLAYSURF = DISPLAYSURF
        self.enemy_tank = enemy_tank
        self.my_tank = my_tank
        self.tank_hit = pygame.mixer.Sound("tank_hit.wav")

    def update(self):
        if self.time_alive > 0:
            if self.color == 'red':
                self.rect.x += self.speed * round(math.cos(self.my_tank.angle_rad), 3)
                self.rect.y += self.speed * round(math.sin(self.my_tank.angle_rad), 3)
                self.time_alive -= 1
                print 'bullet X and Y and angle: %s, %s, %s' % (self.rect.x, self.rect.y, self.angle_rad)
                print 'cos and sin: %s, %s' % (round(math.cos(self.my_tank.angle_rad), 3), round(math.sin(self.my_tank.angle_rad), 3))
                if self.time_alive <= 0:
                    self.rect.x = -100
                    self.rect.y = -100
                    print 'bullets reset'
            if self.color == 'blue':
                self.rect.x += self.speed * round(math.cos(self.my_tank.angle_rad_blue), 3)
                self.rect.y -= self.speed * round(math.sin(self.my_tank.angle_rad_blue), 3)
                self.time_alive -= 1
                print 'bullet X and Y: %s, %s' % (self.rect.x, self.rect.y)
                if self.time_alive <= 0:
                    self.rect.x = -100
                    self.rect.y = -100
                    print 'bullets reset'
        self.tileX = int(self.rect.x / self.game_map.TILESIZE)
        self.tileY = int(self.rect.y / self.game_map.TILESIZE)
        if self.game_map.tilemap[self.tileY][self.tileX] == self.game_map.wall or self.enemy_tank.tileX == \
                self.tileX and self.enemy_tank.tileY == self.tileY:
            self.rect.x = -100
            self.rect.y = -100
            self.time_alive = 0
            if self.enemy_tank.tileX == self.tileX and self.enemy_tank.tileY == self.tileY:
                self.tank_hit.play()
                self.enemy_tank.hit_counter = 30
                self.enemy_tank.hit = True
                self.my_tank.score += 1

    def draw(self):
        self.DISPLAYSURF.blit(self.image, (self.rect.x, self.rect.y))